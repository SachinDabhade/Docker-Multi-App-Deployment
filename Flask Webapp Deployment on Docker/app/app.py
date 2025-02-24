from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

# MySQL connection details
db_config = {
    'host': 'db',  # Name of the MySQL service in docker-compose.yml
    'user': 'root',
    'password': 'password',  # Database password
    'database': 'user_db'  # Database name
}

def check_credentials(username, password):
    try:
        # Connect to the MySQL server
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result is not None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if check_credentials(username, password):
        return "Login successful!"
    else:
        return "Invalid credentials!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
