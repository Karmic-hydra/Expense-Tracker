from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'expenses.db'

def init_db():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    expense_type TEXT,
                    name TEXT,
                    amount REAL
                )
            ''')
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_expense', methods=['POST'])
def add_expense():
    try:
        expense_type = request.form['expense_type']
        name = request.form['name']
        amount = float(request.form['amount'])
        with sqlite3.connect(DATABASE) as conn:
            conn.execute('INSERT INTO expenses (expense_type, name, amount) VALUES (?, ?, ?)', (expense_type, name, amount))
        return '', 201
    except Exception as e:
        return str(e), 400

@app.route('/expenses', methods=['GET'])
def get_expenses():
    try:
        with sqlite3.connect(DATABASE) as conn:
            expenses = conn.execute('SELECT expense_type, name, amount FROM expenses').fetchall()
        return jsonify([{'expense_type': row[0], 'name': row[1], 'amount': row[2]} for row in expenses])
    except Exception as e:
        return str(e), 400

@app.route('/get_tips', methods=['GET'])
def get_tips():
    return 'Try to reduce unnecessary expenses and prioritize your spending.'

if __name__ == '__main__':
    app.run(debug=True)
