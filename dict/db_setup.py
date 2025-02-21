import sqlite3

# Connect to SQLite (creates a file if it doesn't exist)
conn = sqlite3.connect("greek_dict.db")

# Create a cursor object
cursor = conn.cursor()

print("Connected to SQLite database successfully!")

with open('dict.sql', 'r') as f:
    sql_script = f.read()
    
    cursor.executescript(sql_script)  # For SQLite
    conn.commit()
    print("SQL script executed successfully!")