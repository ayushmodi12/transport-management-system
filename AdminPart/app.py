# from prettytable import PrettyTable
# import sqlparse
# from flask import Flask, render_template, request
# import mysql.connector
# import difflib

# app = Flask(__name__)

# # Function to connect to MySQL database
# def connect_to_database(host, user, password, database):
#     try:
#         conn = mysql.connector.connect(
#             host=host,
#             user=user,
#             password=password,
#             database=database
#         )
#         return conn
#     except mysql.connector.Error as e:
#         print(f"Error connecting to database: {e}")
#         return None

# # Function to execute a MySQL query and return results
# def execute_query(conn, query):
#     try:
#         cursor = conn.cursor()
#         cursor.execute(query)
#         result = cursor.fetchall()
#         conn.commit()
#         return 0,result
#     except mysql.connector.Error as e:
#         print(f"Error executing query: {e}")
#         return -1,e

# def parse_query(query):
#     try:
#         # Parse the SQL query
#         parsed_query = sqlparse.parse(query)

#         # Extract table names from the parsed query
#         table_names = set()
#         for stmt in parsed_query:
#             for token in stmt.tokens:
#                 if isinstance(token, sqlparse.sql.IdentifierList):
#                     for identifier in token.get_identifiers():
#                         table_names.add(str(identifier))
#                 elif isinstance(token, sqlparse.sql.Identifier):
#                     table_names.add(str(token))
#         return table_names
#     except Exception as e:
#         print(f"Error parsing query: {e}")
#         return None
    
# # Function to get field names of a table
# def get_field_names(conn, table_name):
#     try:
#         query = f"SHOW COLUMNS FROM {table_name}"
#         cursor = conn.cursor()
#         cursor.execute(query)
#         field_names = [row[0] for row in cursor.fetchall()]
#         return field_names
#     except mysql.connector.Error as e:
#         print(f"Error getting field names: {e}")
#         return None

# def table_diff(before_file_path, after_file_path, diff_file_path):
#     with open(before_file_path, 'r') as before_file:
#         before_content = before_file.read().splitlines()
    
#     with open(after_file_path, 'r') as after_file:
#         after_content = after_file.read().splitlines()

#     diff = difflib.HtmlDiff().make_file(before_content, after_content,"BEFORE THE QUERY WAS EXECUTED", "AFTER THE QUERY WAS EXECUTED")

#     with open(diff_file_path, 'w') as diff_file:
#         diff_file.write(diff)

# def makeASCII(query_result, field_names, file_path):
#     if not query_result:
#         return None

#     table = PrettyTable()
#     table.field_names = field_names

#     for row in query_result:
#         table.add_row(row)

#     with open(file_path, 'w') as f:
#         f.write(str(table))

# # Route to display the main page
# @app.route('/')
# def main_page():
#     return render_template('index.html')

# # Route to execute the query and display results
# @app.route('/execute_query', methods=['POST'])
# def execute_and_display():
#     conn = connect_to_database('localhost', 'root', '1234', 'transportmanagement')
#     query = request.form['sql_query']
#     table_name = parse_query(query).pop()
#     table_fields = get_field_names(conn, table_name)
#     before_path = r'AdminPart\tmp\before.txt'
#     after_path = r'AdminPart\tmp\after.txt'
#     diff_path = r'AdminPart\templates\diff.html'
#     before_query = after_query = f"SELECT * FROM {table_name}"
#     before_result = execute_query(conn, before_query)
#     if (before_result[0] == -1):
#         return "ERROR IN EXECUTING QUERY TO FETCH STARTNG STATE OF THE TABLE --> " + str(before_result[1])
    
#     makeASCII(before_result[1], table_fields, before_path)
#     res = execute_query(conn, query)

#     if (res[0] == -1):
#         return "ERROR IN EXECUTING QUERY --> " + str(res[1])
    
#     after_result = execute_query(conn, after_query)
#     if (after_result[0] == -1):
#         return "ERROR IN EXECUTING QUERY TO FETCH CHANGED STATE OF THE TABLE --> " + str(after_result[1])
    
#     makeASCII(after_result[1], table_fields, after_path)
#     table_diff(before_path, after_path, diff_path)
#     conn.close()
#     return render_template('diff.html')
#         # Diff path now stores the path of the file containing the diffte query."

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, render_template, request, jsonify
# import mysql.connector

# app = Flask(__name__)

# # Function to establish database connection
# def connect_to_database():
#     try:
#         # Replace 'your_host', 'your_username', 'your_password', and 'your_database' with actual values
#         connection = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password='1234',
#             database='transportmanagement'
#         )
#         print("Connected to database")
#         return connection
#     except mysql.connector.Error as error:
#         print("Error connecting to database:", error)
#         return None

# # Execute SQL query
# def execute_sql_query(query):
#     connection = connect_to_database()
#     if connection:
#         try:
#             cursor = connection.cursor(dictionary=True)
#             cursor.execute(query)
#             result = cursor.fetchall()
#             connection.commit()
#             cursor.close()
#             connection.close()
#             return result
#         except mysql.connector.Error as error:
#             print("Error executing SQL query:", error)
#             return None
#     else:
#         return None

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/execute_sql', methods=['POST'])
# def execute_sql():
#     query = request.json['query']
#     result = execute_sql_query(query)
#     if result is not None:
#         return jsonify({'success': True, 'data': result})
#     else:
#         return jsonify({'success': False, 'message': 'Error executing SQL query'})

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request
import mysql.connector
from diff_match_patch import diff_match_patch

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
        return 0,result
    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")
        return -1,e

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

# Function to calculate table difference using diff_match_patch library
def calculate_table_diff(before_result, after_result):
    dmp = diff_match_patch()
    diff = dmp.diff_main(str(before_result), str(after_result))
    dmp.diff_cleanupSemantic(diff)
    # print(diff)
    return dmp.diff_prettyHtml(diff)

def parse_query(query):
    tokens = query.split()
    if (tokens[0].lower() == 'select'):
        for i in range(len(tokens)):
            if (tokens[i].lower() == 'from'):
                return tokens[i+1]
    
    elif (tokens[0].lower() == 'update'):
        return tokens[1]
    
    elif (tokens[0].lower() == 'delete'):
        return tokens[2]
    
    elif (tokens[0].lower() == 'insert'):
        return tokens[2]
    else:
        return "Query is not supported"
    


from flask import Flask, render_template, request
import mysql.connector
from diff_match_patch import diff_match_patch

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
        return 0, result
    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")
        return -1, e

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

# Function to calculate table difference using diff_match_patch library
def calculate_table_diff(before_result, after_result):
    dmp = diff_match_patch()
    diff = dmp.diff_main(str(before_result), str(after_result))
    dmp.diff_cleanupSemantic(diff)
    return dmp.diff_prettyHtml(diff)

def parse_query(query):
    tokens = query.split()
    if (tokens[0].lower() == 'select'):
        for i in range(len(tokens)):
            if (tokens[i].lower() == 'from'):
                return tokens[i+1]
    else:
        return None

# Route to display the main page
@app.route('/')
def main_page():
    return render_template('index.html')

# Route to execute the query and display results
@app.route('/execute_query', methods=['POST'])
def execute_and_display():
    conn = connect_to_database('localhost', 'root', '1234', 'transportmanagement')
    query = request.form['sql_query']
    
    # Parse query to determine table name for select queries
    table_name = parse_query(query)
    
    if table_name:
        # Execute select query
        res = execute_query(conn, query)
        if res[0] == -1:
            return "ERROR IN EXECUTING QUERY --> " + str(res[1])
        
        # Get field names for table header
        table_fields = get_field_names(conn, table_name)
        
        # Render select output template
        return render_template('select_output.html', table_data=res[1], table_fields=table_fields)
    else:
        # Execute non-select query
        before_query = after_query = f"SELECT * FROM {table_name}"
        before_result = execute_query(conn, before_query)
        if before_result[0] == -1:
            return "ERROR IN EXECUTING QUERY TO FETCH STARTNG STATE OF THE TABLE --> " + str(before_result[1])
        
        # Execute the query
        res = execute_query(conn, query)
        if res[0] == -1:
            return "ERROR IN EXECUTING QUERY --> " + str(res[1])
        
        # Fetch changed state of the table
        after_result = execute_query(conn, after_query)
        if after_result[0] == -1:
            return "ERROR IN EXECUTING QUERY TO FETCH CHANGED STATE OF THE TABLE --> " + str(after_result[1])
        
        # Calculate table difference
        table_diff_html = calculate_table_diff(before_result[1], after_result[1])
        
        # Render diff output template
        return render_template('diff_output.html', table_diff=table_diff_html)

if __name__ == '__main__':
    app.run(debug=True)
