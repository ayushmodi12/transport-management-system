from prettytable import PrettyTable
import sqlparse
from flask import Flask, render_template, request
import mysql.connector
import difflib

app = Flask(__name__)

# Function to connect to MySQL database
def connect_to_database(host, user, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Function to execute a MySQL query and return results
def execute_query(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        return result
    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")
        return None

def parse_query(query):
    try:
        # Parse the SQL query
        parsed_query = sqlparse.parse(query)

        # Extract table names from the parsed query
        table_names = set()
        for stmt in parsed_query:
            for token in stmt.tokens:
                if isinstance(token, sqlparse.sql.IdentifierList):
                    for identifier in token.get_identifiers():
                        table_names.add(str(identifier))
                elif isinstance(token, sqlparse.sql.Identifier):
                    table_names.add(str(token))
        return table_names
    except Exception as e:
        print(f"Error parsing query: {e}")
        return -1
    
# Function to get field names of a table
def get_field_names(conn, table_name):
    try:
        query = f"SHOW COLUMNS FROM {table_name}"
        cursor = conn.cursor()
        cursor.execute(query)
        field_names = [row[0] for row in cursor.fetchall()]
        return field_names
    except mysql.connector.Error as e:
        print(f"Error getting field names: {e}")
        return None

def table_diff(before_file_path, after_file_path, diff_file_path):
    with open(before_file_path, 'r') as before_file:
        before_content = before_file.read().splitlines()
    
    with open(after_file_path, 'r') as after_file:
        after_content = after_file.read().splitlines()

    diff = difflib.HtmlDiff().make_file(before_content, after_content,"BEFORE THE QUERY WAS EXECUTED", "AFTER THE QUERY WAS EXECUTED")

    with open(diff_file_path, 'w') as diff_file:
        diff_file.write(diff)

def makeASCII(query_result, field_names, file_path):
    if not query_result:
        return None

    table = PrettyTable()
    table.field_names = field_names

    for row in query_result:
        table.add_row(row)

    with open(file_path, 'w') as f:
        f.write(str(table))

# Route to display the main page
@app.route('/')
def main_page():
    return render_template('index.html')

# Route to execute the query and display results
@app.route('/execute_query', methods=['POST'])
def execute_and_display():
    conn = connect_to_database('localhost', 'root', '1234', 'transportmanagement')
    query = request.form['sql_query']
    table_name = parse_query(query).pop()
    table_fields = get_field_names(conn, table_name)
    before_path = 'before.txt'
    after_path = 'after.txt'
    diff_path = './templates/diff.html'
    before_query = after_query = f"SELECT * FROM {table_name}"
    before_result = execute_query(conn, before_query)
    makeASCII(before_result, table_fields, before_path)
    res = execute_query(conn, query)
    if (res == -1):
        return "ERRRO IN EXECUTING QUERY"
    
    after_result = execute_query(conn, after_query)
    makeASCII(after_result, table_fields, after_path)
    table_diff(before_path, after_path, diff_path)
    return render_template('diff.html')
        # Diff path now stores the path of the file containing the diffte query."

if __name__ == '__main__':
    app.run(debug=True)


