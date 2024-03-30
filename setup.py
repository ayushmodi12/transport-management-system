import getpass
import os
import subprocess
import sys

def execute_sql_file(host, user, password, sql_file):
    # Build the MySQL command
    
    mysql_path = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
    mysql_command = f'"{mysql_path}" --host={host} --user={user} --password={password} < "{sql_file}"'
    # Execute SQL commands from the file
    try:
        subprocess.run(mysql_command, shell=True, check=True)
        print("Database and tables created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to create database and tables: {e}")
        return False

    return True

# Prompt the user for database connection details
print("<<<<<<<<<<<<<<<<<<<<<<< SETTING UP DATABASE >>>>>>>>>>>>>>>>>>>>>")
host = input("Enter the database host: ")
user = input("Enter the database user: ")
password = getpass.getpass("Enter the database password (The password will be hidden as you type): ")  # Hide password input
sql_file = "DatabaseFiles/transport_management_system.sql"

# Check if the SQL file exists
if not os.path.exists(sql_file):
    print(f"Error: The SQL file '{sql_file}' does not exist.")
    exit(1)

# Execute SQL commands from the file
if not execute_sql_file(host, user, password, sql_file):
    exit(1)
print("<<<<<<<<<<<<<<<<<<<<<<< DATABASE SETUP COMPLETE >>>>>>>>>>>>>>>>>>>>>")

# Start the Flask application
print("<<<<<<<<<<<<<<<<<<<<<<< RUNNING FLASK APPLICATION >>>>>>>>>>>>>>>>>>>>>")
try:
    # Detect the path to python executable
    py_path = sys.executable
    subprocess.run([py_path, "transport_management_system.py", f"--host={host}", f"--password={password}", f"--user={user}"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error: Failed to start Flask application: {e}")
