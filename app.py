from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from langchain_google_vertexai import VertexAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain 
import os

app = Flask(__name__)

# Database setup 
conn = sqlite3.connect('expenses.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL, 
        amount INTEGER NOT NULL
    )
''')
conn.commit()

# Set environment variable for service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/gluonparticle/Downloads/springbird-b8e6be1b36fb.json"

# Initialize your LLM (example using Vertex AI)
llm = VertexAI(project="springbird", location="us-central1", model_name="text-bison@001")

# Create a prompt template
prompt_template = PromptTemplate(
    input_variables=["expenses"],
    template="Analyze the following expense report and provide some suggestions for improvement:\n\n{expenses} \n \n Please give me some suggestions based on the expenses below:\n\n  I want suggestions based on where I am spending more, how I can save money, and how I can improve my spending habits, how to keep myself healthy, lower calorie intake \n\n Suggestions:"
)

# Create an LLM chain
llm_chain = LLMChain(llm=llm, prompt=prompt_template)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'name' in request.form:
        name = request.form['name']
        price = float(request.form['price'])
        amount = int(request.form['amount'])

        # Insert expense into database
        cursor.execute('INSERT INTO expenses (name, price, amount) VALUES (?, ?, ?)', (name, price, amount))
        conn.commit()

        return redirect(url_for('index'))

    elif request.method == 'POST' and 'get_suggestions' in request.form:
        # Get expenses from the database
        cursor.execute('SELECT * FROM expenses')
        expenses = cursor.fetchall()

        # Format expenses as a string (adjust formatting if needed)
        expenses_string = ""
        for expense in expenses:
            expenses_string += f"ID: {expense[0]}, Name: {expense[1]}, Price: {expense[2]}, Amount: {expense[3]}, Total: {expense[2] * expense[3]}\n"

        # Run the LLM chain with the expenses as input
        response = llm_chain.run(expenses=expenses_string)

        # Extract suggestions from the LLM response (adjust based on response format)
        suggestions = extract_suggestions_from_response(response) 

        return render_template('index.html', expenses=expenses, suggestions=suggestions)

    # Fetch expenses from database (for initial display)
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    return render_template('index.html', expenses=expenses)

def extract_suggestions_from_response(response):
    # Assuming the LLM response is a string with suggestions separated by newlines
    return response.strip().split('\n')

if __name__ == '__main__':
    app.run(debug=True)