import sqlite3

connection = sqlite3.connect('example.db')

cursor = connection.cursor()

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    department TEXT NOT NULL,
    salary REAL
    )
    '''
)

connection.commit()

query = '''
INSERT INTO employees (name, position, department, salary) VALUES (?, ?, ?, ?)
'''

cursor.execute(query, ('John', 'Software Engineer', 'IT', 70000.00))

connection.commit()

cursor.execute('SELECT * FROM employees')

connection.commit()

rows = cursor.fetchall()

for row in rows:
    print(row)

    print("UPDATE INFO\n\n")

update_query='''
UPDATE employees SET salary = ? WHERE id = ?
'''

cursor.execute(update_query, (75000, 1))

connection.commit()

cursor.execute('SELECT * FROM employees')

connection.commit()

rows = cursor.fetchall()

for row in rows:
    print(row)

