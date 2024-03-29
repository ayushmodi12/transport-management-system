import os
from prettytable import PrettyTable
from diff_match_patch import diff_match_patch
import re
import difflib
import mysql.connector

def query_result_to_file(query_result, field_names, file_path):
    if not query_result:
        return None

    table = PrettyTable()
    table.field_names = field_names

    for row in query_result:
        table.add_row(row)

    with open(file_path, 'w') as f:
        f.write(str(table))

    return file_path


    
def generate_table_diff(before_file_path, after_file_path):
    # Read the contents of the before and after files
    with open(before_file_path, 'r') as before_file:
        before_content = before_file.read().splitlines()
    
    with open(after_file_path, 'r') as after_file:
        after_content = after_file.read().splitlines()
    
    # Compute the differences
    diff = difflib.HtmlDiff().make_file(before_content, after_content,)
    
    # Write the diff to a new file
    with open('diff.html', 'w') as diff_file:
        diff_file.write(diff)
        


'''
Can you create a function that takes the list of tupples that are the output from the execution of a mysql query. Then creates a txt file that stores this output as a ASCII table using pretty tables or a better library. The function should return the file path in which the ASCII table is stored.  

Then create another function that takes the path of two files, before and after. Then uses diff_match_patch to to generate the ouptut and stores it in another txt file. In the proper fashion. Green addidions, Red strike through deletes and updates. 
'''


def connect_to_database(host, user, password, database):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return conn

def execute_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def extract_table_name(query):
    match = re.search(r'into\s+(\w+)', query, re.I)
    if match:
        return match.group(1)
    else:
        return None

def get_field_names(conn, table_name):
    query = f"SHOW COLUMNS FROM {table_name}"
    result = execute_query(conn, query)
    field_names = [row[0] for row in result]
    return field_names

conn = connect_to_database('localhost', 'root', '1234', 'ToBeDeleted')
query1 = "Select * from A"
query2 = "Insert into A values (3, 'Vedant Kumbhar')"
query3 = "Update A set name = 'Mithil Pechmuthu' where Num = 2"

table_name = extract_table_name(query2)
field_names = get_field_names(conn, table_name)
before = execute_query(conn, query1)
print(before)
before_file_path = query_result_to_file(before, field_names, 'before.txt')
print(before_file_path)
_ = execute_query(conn, query2)
after = execute_query(conn, query1)
print(after)
after_file_path = query_result_to_file(after, field_names, 'after.txt')
print(after_file_path)
diff_file_path = generate_table_diff(before_file_path, after_file_path)
print(diff_file_path)

conn.close()
