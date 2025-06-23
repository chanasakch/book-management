# ==========================
# Database Check Script
# ==========================
import sqlite3

# Open a connection to the SQLite database
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

# Check if the 'users' table exists in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
if cursor.fetchone():
    print("Table 'users' exists.")  # Table exists
else:
    print("Table 'users' does not exist.")  # Table does not exist

# Close the database connection
conn.close()