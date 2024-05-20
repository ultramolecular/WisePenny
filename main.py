import sqlite3
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        date TEXT NOT NULL,
        descr TEXT NOT NULL,
        amount REAL NOT NULL,
        method TEXT NOT NULL,
        category TEXT NOT NULL,
        type TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS balance (
        id INTEGER PRIMARY KEY,
        cash_balance REAL NOT NULL,
        checking_balance REAL NOT NULL
    )''')
    c.execute("INSERT OR IGNORE INTO balance (id, cash_balance, checking_balance) VALUES (1, 0.0, 0.0)")
    conn.commit()
    conn.close()

def add_funds(amount, method):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    if method.lower() == 'cash':
        c.execute("UPDATE balance SET cash_balance = cash_balance + ? WHERE id = 1", (amount,))
    elif method == 'checking':
        c.execute("UPDATE balance SET checking_balance = checking_balance + ? WHERE id = 1", (amount,))
    conn.commit()
    conn.close()
    print(f"Added ${amount} to {method} balance.")

def get_balance():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT cash_balance, checking_balance FROM balance WHERE id = 1")
    balances = c.fetchone()
    conn.close()
    return balances

def view_balance():
    cash_balance, checking_balance = get_balance()
    total_balance = cash_balance + checking_balance
    print(f"Current available balance is: ${total_balance:.2f}")
    print(f"Breakdown: Cash = ${cash_balance:.2f}, Checking = ${checking_balance:.2f}")

def add_expense(date, descr, amount, method, category, tpe):
    cash_balance, checking_balance = get_balance()
    total_balance = cash_balance + checking_balance
    if amount > total_balance:
        print("Insufficient funds. Expense not added.")
        return

    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (date, descr, amount, method, category, type) VALUES (?, ?, ?, ?, ?, ?)",
              (date, descr, amount, method, category, tpe))
    if method.lower() == 'cash':
        if amount > cash_balance:
            print("Insufficient cash funds. Expense not added.")
            conn.rollback()
            conn.close()
            return
        c.execute("UPDATE balance SET cash_balance = cash_balance - ? WHERE id = 1", (amount,))
    else:
        if amount > checking_balance:
            print("Insufficient checking funds. Expense not added.")
            conn.rollback()
            conn.close()
            return
        c.execute("UPDATE balance SET checking_balance = checking_balance - ? WHERE id = 1", (amount,))
    conn.commit()
    conn.close()
    print("Expense logged successfully!")

def remove_expense(exp_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT amount, method FROM expenses WHERE id=?", (exp_id,))
    expense = c.fetchone()
    if expense:
        amount, method = expense
        c.execute("DELETE FROM expenses WHERE id=?", (exp_id,))
        if method.lower() == 'cash':
            c.execute("UPDATE balance SET cash_balance = cash_balance + ? WHERE id = 1", (amount,))
        else:
            c.execute("UPDATE balance SET checking_balance = checking_balance + ? WHERE id = 1", (amount,))
        conn.commit()
        conn.close()
        print(f"Expense with ID {exp_id} removed successfully.")
    else:
        print(f"Expense not found.")

def edit_expense(exp_id, descr=None, amount=None, method=None, category=None, tpe=None):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    fields, values = [], []

    if descr:
        fields.append("descr=?")
        values.append(descr)
    if amount:
        fields.append("amount=?")
        values.append(amount)
    if method:
        fields.append("method=?")
        values.append(method)
    if category:
        fields.append("category=?")
        values.append(category)
    if tpe:
        fields.append("type=?")
        values.append(tpe)

    values.append(exp_id)
    c.execute(f"UPDATE expenses SET {', '.join(fields)} WHERE id=?", values)
    conn.commit()
    conn.close()
    print(f"Expense with ID {exp_id} edited successfully.")

def view_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()
    conn.close()

    header = ['ID', 'Date', 'Description', 'Amount', 'Method', 'Category', 'Type']
    print(f"{header[0]:<5} {header[1]:<12} {header[2]:<30} {header[3]:<10} {header[4]:<15} {header[5]:<15} {header[6]:<10}")
    print("="*97)

    for exp in expenses:
        print(f"{exp[0]:<5} {exp[1]:<12} {exp[2]:<30} {exp[3]:<10.2f} {exp[4]:<15} {exp[5]:<15} {exp[6]:<10}")

def analyze_expenses():
    conn = sqlite3.connect('expenses.db')
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()

    cash_balance, checking_balance = get_balance()
    total_balance = cash_balance + checking_balance
    total_expenses = df['amount'].sum()
    total_funds = total_balance + total_expenses

    if total_funds == 0:
        print("No funds available for analysis.")
        return

    needs = df[df['type'] == 'Need']['amount'].sum() / total_funds * 100
    wants = df[df['type'] == 'Want']['amount'].sum() / total_funds * 100
    savings = df[df['type'] == 'Savings and Debt']['amount'].sum() / total_funds * 100

    print(f"Total funds: ${total_funds:.2f}")
    print(f"Available Balance: ${total_balance:.2f}")

    labels = ['Needs', 'Wants', 'Savings and Debt']
    sizes = [needs, wants, savings]
    colors = ['#ff9999', '#66b3ff', '#99ff99']

    plt.pie(sizes, labels = labels, colors = colors, autopct = '%1.1f%%', startangle = 140)
    plt.axis('equal')
    plt.title('Expense Distribution (50/30/20 Rule)')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description = "Expense Tracker")
    subparsers = parser.add_subparsers(dest = "command")
    
    add_parser = subparsers.add_parser("add", help = "Add a new expense")
    add_parser.add_argument("date", type = str, help = "Date of the expense in YYYY-MM-DD format")
    add_parser.add_argument("descr", type = str, help = "Description of the expense")
    add_parser.add_argument("amount", type = float, help = "Amount of the expense in dollars")
    add_parser.add_argument("method", type = str, help = "Method of payment (debit, credit, cash, etc)")
    add_parser.add_argument("category", type = str, help = "Category of the expense (rent, vehicle, groceries, etc)")
    add_parser.add_argument("type", type = str, help = "Type of the expense under the 50/30/20 rule")

    view_parser = subparsers.add_parser("view", help = "View all the expenses")
    view_bal_parser = subparsers.add_parser("view_bal", help = "View the available balance")

    analyze_parser = subparsers.add_parser("analyze", help = "Analyze expenses")

    remove_parser = subparsers.add_parser("remove", help = "Remove an expense by ID")
    remove_parser.add_argument("id", type = int, help = "ID of the expense to be removed")

    edit_parser = subparsers.add_parser("edit", help = "Edit an expense by ID")
    edit_parser.add_argument("id", type = int, help = "ID of the expense to edit")
    edit_parser.add_argument("--descr", type = str, help = "New description of the expense")
    edit_parser.add_argument("--amount", type = float, help = "New amount of the expense")
    edit_parser.add_argument("--method", type = str, help = "New method of payment")
    edit_parser.add_argument("--category", type = str, help = "New category of the expense")
    edit_parser.add_argument("--type", type = str, help = "New type of the expense under 50/30/20 rule")

    add_funds_parser = subparsers.add_parser("add_funds", help = "Add funds to the balance")
    add_funds_parser.add_argument("amount", type = float, help = "Amount to add to the balance")
    add_funds_parser.add_argument("method", type = str, help = "Method of adding funds (cash, checking)")
    
    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.date, args.descr, args.amount, args.method, args.category, args.type)
    elif args.command == "remove":
        remove_expense(args.id)
    elif args.command == "edit":
        edit_expense(args.id, args.descr, args.amount, args.method, args.category, args.type)
    elif args.command == "view":
        view_expenses()
    elif args.command == "view_bal":
        view_balance()
    elif args.command == "analyze":
        analyze_expenses()
    elif args.command == "add_funds":
        add_funds(args.amount, args.method)

if __name__ == "__main__":
    init_db()
    main()
