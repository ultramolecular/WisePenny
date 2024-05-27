import os
from datetime import timedelta
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
from flask_session import Session
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Load environment variables
env_path = Path('.') / 'env'
load_dotenv(dotenv_path = env_path)

app = Flask(__name__, static_folder = '../frontend/build', static_url_path = '/')
CORS(app, supports_credentials = True)

app.secret_key = os.getenv('REACT_APP_SECRET_KEY')

app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days = 1)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
Session(app)

# Firebase setup
cred_path = os.getenv('REACT_APP_FIREBASE_CREDENTIALS_PATH', '../wisepenny_fb.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/login', methods = ['POST'])
def login():
    id_token_str = request.json['idToken']
    try:
        decoded_token = auth.verify_id_token(id_token_str)
        uid = decoded_token['uid']
        session.permanent = True
        session['user_id'] = uid
        return jsonify({"message": "Login successful!"}), 200
    except ValueError:
        return jsonify({"message": "Invalid token!"}), 400

@app.route('/logout', methods = ['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logout successful!"}), 200

@app.route('/add_funds', methods = ['POST'])
def add_funds():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    user_id = session['user_id']
    amount = float(request.json['amount'])
    method = request.json['method']

    user_ref = db.collection('users').document(user_id)
    user_data = user_ref.get().to_dict() or {}

    if method.lower() == 'cash':
        new_bal = user_data.get('cash_balance', 0) + amount
        user_ref.set({'cash_balance': new_bal}, merge = True)
    elif method.lower() == 'checking':
        new_bal = user_data.get('checking_balance', 0) + amount
        user_ref.set({'checking_balance': new_bal}, merge = True)

    return jsonify({"message": "Funds added successfully!"}), 200

@app.route('/add_expense', methods = ['POST'])
def add_expense():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    user_id = session['user_id']
    date = request.json['date']
    descr = request.json['descr']
    amount = float(request.json['amount'])
    method = request.json['method']
    category = request.json['category']
    tpe = request.json['type']

    user_ref = db.collection('users').document(user_id)
    user_data = user_ref.get().to_dict() or {}

    if method.lower() == 'cash':
        if amount > user_data.get('cash_balance', 0):
            return jsonify({"message": "Insufficient cash funds!"}), 400
        new_bal = user_data.get('cash_balance', 0) - amount
        user_ref.set({'cash_balance': new_bal}, merge = True)
    else:
        if amount > user_data.get('checking_balance', 0):
            return jsonify({"message": "Insufficient checking funds"}), 400
        new_bal = user_data.get('checking_balance', 0) - amount
        user_ref.set({'checking_balance': new_bal}, merge = True)

    expense_ref = user_ref.collection('expenses').document()
    expense_ref.set({
        'date': date,
        'descr': descr,
        'amount': amount,
        'method': method,
        'category': category,
        'type': tpe
    })

    return jsonify({"message": "Expense added successfully"}), 200

@app.route('/view_balance', methods = ['GET'])
def view_balance():
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    user_id = session['user_id']
    user_ref = db.collection('users').document(user_id)
    user_data = user_ref.get().to_dict() or {}

    return jsonify({
        "cash_balance": user_data.get('cash_balance', 0),
        "checking_balance": user_data.get('checking_balance', 0),
        "total_balance": user_data.get('cash_balance', 0) + user_data.get('checking_balance', 0)
    }), 200

@app.route('/remove_expense/<string:exp_id>', methods = ['POST'])
def remove_expense(exp_id):
    # if 'user_id' not in session:
    #     return jsonify({"message": "Not authenticated"}), 401

    # user_id = session['user_id']
    # user_ref = db.collection('users').document(user_id)
    # expense_ref = user_ref.collection('expenses').document(exp_id)

    # expense_ref.delete()
    
    # return jsonify({"message": f"Expense with ID {exp_id} removed successfully"}), 200
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    user_id = session['user_id']
    user_ref = db.collection('users').document(user_id)
    expense_ref = user_ref.collection('expenses').document(exp_id)

    print(f"Attempting to delete expense with ID: {exp_id} for user: {user_id}")

    try:
        expense_ref.delete()
        print(f"Successfully deleted expense with ID: {exp_id}")
        return jsonify({"message": f"Expense with ID {exp_id} removed successfully"}), 200
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"message": "An error occurred while deleting the expense", "error": str(e)}), 500

@app.route('/edit_expense/<string:exp_id>', methods = ['POST'])
def edit_expense(exp_id):
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    user_id = session['user_id']
    user_ref = db.collection('users').document(user_id)
    expense_ref = user_ref.collection('expenses').document(exp_id)

    update_data = {key: request.form[key] for key in request.form if request.form[key]}

    expense_ref.update(update_data)

    return jsonify({"message": f"Expense with ID {exp_id} edited successfully!"})

@app.route('/view_expenses')
def view_expenses():
    # TODO: return document ids in the response?
    if 'user_id' not in session:
        return jsonify({"message": "Not authenticated"}), 401

    user_id = session['user_id']
    expenses_ref = db.collection('users').document(user_id).collection('expenses')
    expenses = [doc.to_dict() for doc in expenses_ref.stream()]

    return jsonify(expenses), 200

@app.route('/analyze_expenses')
def analyze_expenses():
    # TODO: see about where this should be and what it should do...
    pass


if __name__ == "__main__":
    app.run(debug = True)
