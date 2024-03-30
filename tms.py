import argparse
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from datetime import datetime
from uuid import uuid4
import difflib
from prettytable import PrettyTable
import sqlparse
import mysql.connector as mconn
from sqlalchemy import text,create_engine
import json


app = Flask(__name__)
app.secret_key = 'your_secret_key'


def driver_details():
    email = session.get('emailID')
    with engine.connect() as conn:
        query = text("SELECT * FROM driver WHERE email_id = :email")
        result = conn.execute(query, {'email': email})
        drivers = result.fetchall()
            
        if drivers:
            columns = result.keys()  # Fetch column names
            req_driver = dict(zip(columns, drivers[0]))
            return req_driver
        else:
            return "No drivers found."


def vehicles_driven():
    info = driver_details()
    license=info['driver_license_number']
    with engine.connect() as conn:
        query1 = text("SELECT * FROM DrivenBy WHERE driver_license_number = :license")
        result1 = conn.execute(query1, {'license': license})
        vehicles = result1.fetchall()
            
        if vehicles:
            columns = result1.keys()  # Fetch column names
            req_vehicles = dict(zip(columns, vehicles[0]))
        else:
            return "No vehicles found."
        
        license_plate_number = req_vehicles['license_plate_number']
        
        query2 = text("SELECT * FROM Vehicle WHERE license_plate_number = :plate")
        result2 = conn.execute(query2, {'plate': license_plate_number})
        vehicles = result2.fetchall()

        if vehicles:
            columns = result2.keys()  # Fetch column names
            required_vehicles = dict(zip(columns, vehicles[0]))
            return required_vehicles['vehicle_type'], license_plate_number
        else:
            return "No vehicles found."       


@app.route('/driver')
def driver():
    info = driver_details()
    vehicle_type, license_plate_number = vehicles_driven()
    bank=json.loads(info['bank_details'])
    ifsc = bank['ifsc_code']
    acc_no = bank['account_number']
    branch = bank['branch_name']
    return render_template('driver.html', name = info['first_name']+' '+info['last_name'],number=info['phone_number'],
                           email_id = info['email_id'], join = info['date_of_joining'], license = info['driver_license_number'],
                           vehicles = vehicle_type+' '+'('+license_plate_number+')',
                           ifsc = 'IFSC Code: '+ifsc,acc='Account Number: '+acc_no,branch='Branch: '+branch)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        option = request.form['option']
        if option == 'login':
            return redirect(url_for('login'))
        elif option == 'signup':
            return redirect(url_for('signup'))
    return render_template('login_signup_index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Fetch form data
        username = request.form['username']
        password = request.form['password']

        # Cursor creation
        cur = mysql.connection.cursor()

        # Execute query
        print(username, password)
        cur.execute("SELECT * FROM users WHERE email = %s AND password = MD5(%s)", (username, password))
        user = cur.fetchone()
        print(user)
        cur.execute("SELECT * FROM Driver WHERE email_id = %s", (username,))
        driver = cur.fetchone()
        print(driver)
        # Close cursor
        cur.close()
        if (user):
            if user[2] == 'no':
                if driver:
                    flash('Welcome Driver', 'success')
                    return redirect(url_for('driver'))
                # User found, redirect to dashboard or profile page
                flash('Login Successful', 'success')
                session['emailID'] = username
                return redirect(url_for('landing'))  # Replace 'dashboard' with your dashboard route
            elif user[2] == 'yes':
                flash('Welcome Admin', 'success')
                return redirect(url_for('admin'))  
        else:
            # User not found or credentials incorrect
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Fetch form data
        username = request.form['username']
        password = request.form['password']

        # Cursor creation
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (username, password))

        # Commit to database
        mysql.connection.commit()

        # Close cursor
        cur.close()

        flash('Signup Successful', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/booking2', methods=['GET', 'POST'])
def booking2():
    if request.method == 'POST':
        # Handle booking submission
        date = request.form['date']
        time_slot = request.form['time_slot']

        # Check if the selected time slot is available
        # Perform database query to check availability
        # If available, book the slot and update the database
        # If not available, display a warning message
        # This logic will be implemented in detail later

        flash('Booking successful!', 'success')
        return redirect(url_for('landing'))

    return render_template('booking2.html')

@app.route('/booking')
def booking():
    # Fetch available buses from the database
    cur = mysql.connection.cursor()
    print(cur)
    cur.execute("SELECT * FROM Vehicle")
    buses = cur.fetchall()
    print("HIIIIIIIIIIIIIIIIIIIIIIII")
    print(buses)
    cur.close()
    
    # Render the template with the list of available buses
    return render_template('index.html', buses=buses)

@app.route('/book-seats', methods=['POST'])
def book_seats():
    # Get selected seat from the request data
    data = request.json
    print(data)
    selected_seat = data.get('selectedSeat')
    print(selected_seat)
    
    # licence_plate_number = data.get('licencePlateNumber')
    date = data.get('_date')
    route = data.get('route')
    c = route[0]
    
    route = route[1:]

    # if not selected_seat or not licence_plate_number:
    #     return jsonify({'error': 'No seat or licence plate number provided'}), 400

    # user_email = 'exampsfle_email@example.com'
    user_email = data.get('userEmail')
    capacity = 0
    if (c == '0'):
        capacity = 56
    else:
        capacity = 29

    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM Booking WHERE _date = %s AND email_id = %s AND route = %s", (date, user_email, route))
    booking_count = cur.fetchone()[0]
    print(booking_count)
    cur.close()

    if booking_count > 0:
        return jsonify({'error': 'You have already booked a ticket for this bus'}), 400

    # Get current date and time
    date_time = datetime.now()
    booking_id = str(uuid4())

    # Insert booking details into the database
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Booking (email_id, booking_id, booked_seat, booking_created, capacity, route, _date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (user_email, booking_id, selected_seat, date_time, capacity, route, date, ))
        mysql.connection.commit()
        cur.close()
        
        msg = Message(subject='Booking Confirmed!', sender='ayushtmodi@gmail.com', recipients=[user_email])
        msg.body = f"Hello, Your Booking has been confirmed. Here are the details: \n\nDate: {date}\nTime and Route: {route}\nBus Details: {capacity}-Seater Bus\nBooked Seat Number: {selected_seat}\n\nThank you!"
        mail.send(msg)
        
        return jsonify({'message': 'Booking successful'}), 200
    except Exception as e:
        print("ACHA")
        print(e)
        return jsonify({'error': str(e)}), 500


@app.route('/fetch-booked-seats', methods=['GET', 'POST'])
def fetch_booked_seats():
    if request.method == 'POST':    
        data = request.json
        date = data.get('_date')
        route = data.get('route')
        c = route[0]
        
        route = route[1:]
        # user_email = data.get('userEmail')
        capacity = 0
        if (c == '0'):
            capacity = 56
        else:
            capacity = 29

        # cursor = db.cursor(dictionary=True)
        cur = mysql.connection.cursor()
        cur.execute("SELECT booked_seat FROM Booking WHERE _date = %s AND route = %s AND capacity = %s", (date, route, capacity))  # Adjust this query as per your database schema
        booked_seats = cur.fetchall()
        print("WORKKKKKKK")
        print(booked_seats)
        cur.close()
        return jsonify({'bookedSeats': booked_seats})
    else:
        print("SEDDD")
        return jsonify({'error': 'Method not allowed'}), 405

@app.route('/cancel-booking', methods=['POST'])
def cancel_booking():
    data = request.json
    # licence_plate_number = data.get('licencePlateNumber')
    user_email = data.get('emailId')
    date = data.get('_date')
    route = data.get('route_id')
    # print(licence_plate_number)
    c = route[0]
    
    route = route[1:]
        # user_email = data.get('userEmail')
    capacity = 0
    if (c == '0'):
        capacity = 56
    else:
        capacity = 29
    print(user_email)

    # if not licence_plate_number or not user_email:
    #     return jsonify({'error': 'Invalid request data'}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT booked_seat FROM Booking WHERE _date = %s AND email_id = %s AND route = %s AND capacity = %s", (date, user_email, route, capacity))
        canceled_seat = cur.fetchall()
        # print("WORKKKKKKK")
        # print(booked_seats)
        print(canceled_seat)
        cur.close()
        print("POPP")
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Booking WHERE _date = %s AND email_id = %s AND route = %s AND capacity = %s", (date, user_email, route, capacity))
        print("POPP2")
        mysql.connection.commit()
        cur.close()
        
        msg = Message(subject='Booking Cancelled', sender='ayushtmodi@gmail.com', recipients=[user_email])
        msg.body = f"Hello, Your Booking for the bus on Date: {date}, Time and Route: {route}, {capacity}-Seater, and Seat Number: {canceled_seat[0][0]} has been cancelled succesfully."
        mail.send(msg)
        
        return jsonify({'canceledSeat': canceled_seat}), 200
    except Exception as e:
        print("LOCHA")
        return jsonify({'error': str(e)}), 500


@app.route('/fetch-users-booked-seat', methods=['GET', 'POST'])
def fetch_users_booked_seat():
    if request.method == 'POST':    
        data = request.json
        date = data.get('_date')
        route = data.get('route')
        c = route[0]
        
        route = route[1:]
        user_email = data.get('userEmail')
        capacity = 0
        if (c == '0'):
            capacity = 56
        else:
            capacity = 29

        # cursor = db.cursor(dictionary=True)
        cur = mysql.connection.cursor()
        cur.execute("SELECT booked_seat FROM Booking WHERE _date = %s AND route = %s AND capacity = %s AND email_id = %s", (date, route, capacity, user_email))  # Adjust this query as per your database schema
        booked_seats = cur.fetchall()
        print("WORKKKKKKK")
        print(booked_seats)
        cur.close()
        return jsonify({'bookedSeats': booked_seats})
    else:
        print("SEDDD")
        return jsonify({'error': 'Method not allowed'}), 405

@app.route('/seat-selection', methods=['GET', 'POST'])
def seat_selection():
    if request.method == 'POST':
        # Retrieve the selected date, route ID, and capacity from the form data
        selected_date = request.form.get('date')
        route_id = request.form.get('time_slot')

        # Redirect to the seat selection page with the selected date, route ID, and capacity as URL parameters
        logged_in_user_email = session.get('emailID')
        return redirect(url_for('seat_selection', date=selected_date, route_id=route_id, logged_in_user_email=logged_in_user_email))
    else:
        # For GET requests, render the seat selection page
        logged_in_user_email = session.get('emailID')
        return render_template('seat_selection.html', logged_in_user_email=logged_in_user_email)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/execute_query', methods=['POST'])
def execute_and_display():
    conn = connect_to_database(host, user, passwd, 'transportmanagement')
    query = request.form['sql_query']
    table_name = parse_query(query).pop()
    table_fields = get_field_names(conn, table_name)
    before_path = r'tmp\before.txt'
    after_path = r'tmp\after.txt'
    diff_path = r'templates\diff.html'
    before_query = after_query = f"SELECT * FROM {table_name}"
    before_result = execute_query(conn, before_query)
    if (before_result[0] == -1):
        return "ERROR IN EXECUTING QUERY TO FETCH STARTNG STATE OF THE TABLE --> " + str(before_result[1])
    
    makeASCII(before_result[1], table_fields, before_path)
    res = execute_query(conn, query)

    if (res[0] == -1):
        return "ERROR IN EXECUTING QUERY --> " + str(res[1])
    
    after_result = execute_query(conn, after_query)
    if (after_result[0] == -1):
        return "ERROR IN EXECUTING QUERY TO FETCH CHANGED STATE OF THE TABLE --> " + str(after_result[1])
    
    makeASCII(after_result[1], table_fields, after_path)
    table_diff(before_path, after_path, diff_path)
    conn.close()
    return render_template('diff.html')
        # Diff path now stores the path of the file containing the diffte query."
    
def connect_to_database(host, user, password, database):
    try:
        conn = mconn.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return conn
    except mconn.Error as e:
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
        return None
    
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
    
def get_args():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Transport Management System")
    parser.add_argument("--host", required=True, help="Database host")
    parser.add_argument("--user", required=True, help="Database user")
    parser.add_argument("--password", required=True, help="Database password")

    args = parser.parse_args()
    host = args.host
    user = args.user
    password = args.password
    return host, user, password

if __name__ == "__main__":
    host,user,passwd = get_args()
    app.config['MYSQL_HOST'] = host
    app.config['MYSQL_USER'] = user
    app.config['MYSQL_PASSWORD'] = passwd
    app.config['MYSQL_DB'] = 'transportmanagement'
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT']= 465
    app.config['MAIL_USERNAME']= 'ayushtmodi@gmail.com'
    app.config['MAIL_PASSWORD']= 'xprz hncd pfwn ttgn'
    app.config['MAIL_USE_TLS']= False
    app.config['MAIL_USE_SSL']= True
    mail = Mail(app)
    mysql = MySQL(app)
    
    engine = create_engine(f"mysql+pymysql://{user}:{passwd}@{host}/TransportManagement?charset=utf8mb4")
    app.run(debug=True)
