# Python code
from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
conn = mysql.connector.connect(user='root',
                                password='user1234',
                                host='localhost',
                                database='library')

@app.route('/data')
def get_data():
  conn.reconnect()
  # Create a cursor
  cursor = conn.cursor(dictionary = True)
  # Execute a SELECT statement
  cursor.execute("SELECT * FROM books")
  # Fetch the rows
  rows = cursor.fetchall()
  cursor.close()
  conn.close()

  # Return the rows as a JSON response
  return jsonify(rows)

@app.route('/add', methods=['POST'])
def add_data():
  conn.reconnect()
  cursor = conn.cursor(dictionary = True)
  # Get the data from the request
  data = request.get_json()

  # Extract the values from the data object
  id = data['id']
  book = data['book']
  author = data['author']

  # Execute an INSERT statement
  cursor.execute("INSERT INTO books (ID, books, Author) VALUES (%s, %s, %s)", (id, book, author))
  conn.commit()
  cursor.close()
  conn.close()

  # Return a success response
  return jsonify({'success': True})

if __name__ == '__main__':
  app.run()
