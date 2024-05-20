# WisePenny

A minimalistic CLI application to log and analyze your expenses based on the 50/30/20 rule.

## Features

- Log expenses with date, description, amount, method, category, and type.
- View all logged expenses.
- Analyze expenses and generate a pie chart showing the distribution of expenses according to the 50/30/20 rule.
- Separate tracking of cash and checking account balances.
- Add funds to either cash or checking account balances.
- View detailed balance breakdown between cash and checking accounts.
- Remove and edit logged expenses.

## Setup

1. Clone the repository:
    ```sh
    git clone git@github.com:user/WisePenny.git
    cd WisePenny
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the application:
    ```sh
    python main.py
    ```

## Usage

### Adding Funds

- Add $50 to the cash balance:
    ```sh
    python main.py add_funds 50 cash
    ```

- Add $100 to the checking account balance:
    ```sh
    python main.py add_funds 100 checking
    ```

### Viewing Balance

- View the current balance and its breakdown:
    ```sh
    python main.py view_bal
    ```

### Adding an Expense

- Add an expense of $25 for groceries paid with cash on 2023-05-19:
    ```sh
    python main.py add 2023-05-19 "Groceries" 25 cash groceries Need
    ```

- Add an expense of $50 for rent paid with checking on 2023-05-20:
    ```sh
    python main.py add 2023-05-20 "Rent" 50 checking rent Need
    ```

### Removing an Expense

- Remove an expense with ID 1:
    ```sh
    python main.py remove 1
    ```

### Editing an Expense

- Edit the description of the expense with ID 2 to "New Groceries":
    ```sh
    python main.py edit 2 --descr "New Groceries"
    ```

- Edit the amount of the expense with ID 3 to $30:
    ```sh
    python main.py edit 3 --amount 30
    ```

### Viewing All Expenses

- View all logged expenses:
    ```sh
    python main.py view
    ```

### Analyzing Expenses

- Analyze the expenses:
    ```sh
    python main.py analyze
    ```

## Current Development To-Do List

### Future Development

1. **Web Application Development**
    - Transition from a CLI application to a web application.
    - Implement user authentication to allow users to log in with their credentials.
    - Store logged expenses securely in the cloud.
    - Develop a web-based interface for logging expenses.
    - Enable users to view and analyze their expenses from any device.

2. **Feature Enhancements**
    - Enable categorization and tagging of expenses for better tracking and reporting.
    - Provide detailed reports and visualizations for financial insights.
    - Implement notifications and reminders for upcoming expenses or budget limits.
    - Integrate with bank APIs to automatically log transactions.

3. **Mobile Application Development**
    - Develop a mobile application for on-the-go expense tracking.
    - Synchronize data between the web and mobile applications.

4. **Improved Analytics**
    - Enhance the analysis features to provide more detailed insights.

