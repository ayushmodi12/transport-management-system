import argparse
import imghdr
import subprocess
import sys
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from datetime import datetime
from uuid import uuid4
import difflib
from prettytable import PrettyTable
from sqlalchemy import text,create_engine
import json
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def driver_details():
    email = session.get('emailID')
    print("HI")
    print(email)
    with engine.connect() as conn:
        query = text("SELECT * FROM driver WHERE email_id = :email")
        # print(email)
        result = conn.execute(query, {'email': email})
        drivers = result.fetchall()
        query2 = text("SELECT user_img FROM users WHERE email = :email")
        image = conn.execute(query2, {'email': email}).fetchall()
        if drivers:
            columns = result.keys()  # Fetch column names
            req_driver = dict(zip(columns, drivers[0]))
            req_driver['user_img'] = image
            return req_driver
        else:
            print("NIMBA")
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
    try:
        vehicle_type, license_plate_number = vehicles_driven()
    except:
        vehicle_type = "No vehicles found."
        license_plate_number = "No vehicles found."

    bank=json.loads(info['bank_details'])
    ifsc = bank['ifsc_code']
    acc_no = bank['account_number']
    branch = bank['branch_name']
    # print(info['user_img'][0][0])
    image_format = imghdr.what(None, info['user_img'][0][0])
    # image_format = 'png'
    image = base64.b64encode(info['user_img'][0][0]).decode('utf-8')
    return render_template('driver.html', name = info['first_name']+' '+info['last_name'],number=info['phone_number'],
                           email_id = info['email_id'], join = info['date_of_joining'], license = info['driver_license_number'],
                           vehicles = vehicle_type+' '+'('+license_plate_number+')',
                           ifsc = 'IFSC Code: '+ifsc,acc='Account Number: '+acc_no,branch='Branch: '+branch,
                           image =image, image_format = image_format)

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
                # User found, redirect to dashboard or profile page
                flash('Login Successful', 'success')
                session['emailID'] = username
                if driver:
                    flash('Welcome Driver', 'success')
                    return redirect(url_for('driver'))
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
        image = request.files['user_image'] if 'user_image' in request.files else None
        print(request.files)
        # Cursor creation
        cursor = mysql.connection.cursor()

        if image:
            # If an image is uploaded, store it in the database
            image_data = image.read()
            cursor.execute("INSERT INTO users (email, password, user_img) VALUES (%s, MD5(%s), %s);",
                           (username, password,image_data))
        else:
            # If no image is uploaded, set iimage column as NULL
            cursor.execute("INSERT INTO users (email, password, user_img) VALUES (%s, MD5(%s), %s);",
                           (username, password,None))


        # Execute query
        # cur.execute("INSERT INTO users (email, password,user_img) VALUES (%s, MD5(%s))", (username, password))

        # Commit to database
        mysql.connection.commit()

        # Close cursor
        cursor.close()

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
    cur.execute("SELECT COUNT(*) FROM Booking WHERE _date = %s AND capacity = %s AND email_id = %s AND route = %s", (date, capacity, user_email, route))
    booking_count = cur.fetchone()[0]
    print(booking_count)
    cur.close()

    if booking_count > 0:
        print("bdoneeee")
        return jsonify({'error': 'You have already booked a ticket for this bus'}), 400

    # Get current date and time
    date_time = datetime.now()
    print(date_time)
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
        print("CRAYYYYY")
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

@app.route('/operation', methods=['POST'])
def handle_operation():
    # operation = request.form['operation']
    
    # Render HTML form for inserting values into tables
    cur = mysql.connection.cursor()
    cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='transportmanagement'")  # Adjust this query as per your database schema
    table_names = cur.fetchall()
    print("WORKKKKKKK")
    print(table_names)
    cur.close()
    # return jsonify({'table_names': table_names})
    # print(j)
    return render_template('view_tables.html', table_names=table_names)

@app.route('/view-tables', methods=['GET', 'POST'])
def view_tables():
    print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
    if request.method == 'POST':
        table_name = request.form['tableName']
        print(table_name)
        # Query the database to fetch the data for the selected table
        # You can use your database access methods here
        # Example: data = query_database(table_name)
        # Pass the data to the template and render it
        cur = mysql.connection.cursor()
        print("A")
        cur.execute(f"select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{table_name}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        columns = cur.fetchall()
        # print("WORKKKKKKK")
        # print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTINGGGGGGGGGOAOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        print(columns)
        print("B")
        # cur.close()
        # cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM {table_name}")  # Adjust this query as per your database schema
        values = cur.fetchall()
        print("WORKKKKKKK")
        print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTINGGGGGGGGGOAOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        print(values)
        
        cur.execute(f"select ORDINAL_POSITION from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{table_name}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        ORDINAL_POSITION = cur.fetchall()
        
        combined = list(zip(columns, ORDINAL_POSITION))

        # Sort the combined list based on the values in ORDINAL_POSITION
        sorted_combined = sorted(combined, key=lambda x: x[1])

        # Extract the sorted columns2 from the sorted_combined list
        columns = [item[0] for item in sorted_combined]
        
        oldcolumns2=columns
        
        cur.close()
        return render_template('display_table.html', columns = columns, oldcolumns2=oldcolumns2, values=values, table_name = table_name, op='view', buttons=True)


@app.route('/insert-values', methods=['GET', 'POST'])
def insert_values():
    if request.method == 'POST':
        table_name = request.form['tableName']
        cur = mysql.connection.cursor()
        cur.execute(f"select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{table_name}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        columns = cur.fetchall()
        
        cur.execute(f"select ORDINAL_POSITION from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{table_name}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        ORDINAL_POSITION = cur.fetchall()
        
        combined = list(zip(columns, ORDINAL_POSITION))

        # Sort the combined list based on the values in ORDINAL_POSITION
        sorted_combined = sorted(combined, key=lambda x: x[1])

        # Extract the sorted columns from the sorted_combined list
        columns = [item[0] for item in sorted_combined]
        
        cur.execute(f"SELECT * FROM {table_name}")  # Adjust this query as per your database schema
        values = cur.fetchall()
        
        cur.close()
        
        return render_template('insert_form.html', columns=columns, table_name=table_name, values = values)
        

@app.route('/submit-values', methods=['POST'])
def submit_values():
    print("00000000000000000000000000000000000000000000000")
    if request.method == 'POST':
        table_name = request.form['tableName']
        
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM {table_name}")  # Adjust this query as per your database schema
        oldvalues = cur.fetchall()
        cur.close()
        
        
        cur = mysql.connection.cursor()
        print("00000000000000000000000000000000000000000000000")
        print(table_name)
        print("1111111111111111111111111111111111111111111111111")
        values = {key: request.form[key] for key in request.form if (key != 'tableName' and request.form[key]!='')}
        
        # Prepare the SQL query for insertion
        placeholders = ', '.join(['%s'] * len(values))
        columns = ', '.join(values.keys())
        print(columns)
        print(values)
        u = tuple(values.values())
        print(u)
        if table_name.lower() == 'users':
            values['password'] = f"MD5('{values['password']}')"
            
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        print(sql)
        error = None
        try:
            cur.execute(sql, u)
            mysql.connection.commit()
            print("HORAAHH")
            flash('Values successfully inserted into the database!', 'success')
        except Exception as e:
            mysql.connection.rollback()
            print("NAHHHHHHHHHHH")
            print(str(e))
            error = str(e)
            flash(f'Error inserting values: {str(e)}', 'error')
        # Execute the query
        cur.close()
        
        
        print("A")
        
        cur = mysql.connection.cursor()
        
        cur.execute(f"select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{table_name}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        columns2 = cur.fetchall()
        
        cur.execute(f"select ORDINAL_POSITION from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{table_name}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        ORDINAL_POSITION = cur.fetchall()
        
        combined = list(zip(columns2, ORDINAL_POSITION))

        # Sort the combined list based on the values in ORDINAL_POSITION
        sorted_combined = sorted(combined, key=lambda x: x[1])

        # Extract the sorted columns2 from the sorted_combined list
        columns2 = [item[0] for item in sorted_combined]
        
        cur.execute(f"SELECT * FROM {table_name}")  # Adjust this query as per your database schema
        values = cur.fetchall()
        print("WORKKKKKKK")
        print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTINGGGGGGGGGOAOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        print(values)
        # try:
        #     cur.execute(sql, u)
        #     mysql.connection.commit()
        #     print("HORAAHH")
        #     flash('Values successfully inserted into the database!', 'success')
        # except Exception as e:
        #     mysql.connection.rollback()
        #     print("NAHHHHHHHHHHH")
        #     print(str(e))
        #     flash(f'Error inserting values: {str(e)}', 'error')
        cur.close()
        
        oldcolumns2=columns2
        
        # Redirect to the view-tables page to display the updated table
        return render_template('display_table.html', table_name=table_name, columns=columns2, oldcolumns2=oldcolumns2, values=values, oldvalues=oldvalues, error = error, op='insert')

@app.route('/update-values', methods=['GET', 'POST'])
def update_values():
    if request.method == 'POST':
        table_name = request.form['tableName']
        cur = mysql.connection.cursor()
        print("A")
        cur.execute(f"select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{table_name}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        columns = cur.fetchall()
        
        cur.execute(f"select ORDINAL_POSITION from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{table_name}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        ORDINAL_POSITION = cur.fetchall()
        
        combined = list(zip(columns, ORDINAL_POSITION))

        # Sort the combined list based on the values in ORDINAL_POSITION
        sorted_combined = sorted(combined, key=lambda x: x[1])

        # Extract the sorted columns from the sorted_combined list
        columns = [item[0] for item in sorted_combined]
        
        cur.execute(f"SELECT * FROM {table_name}")  # Adjust this query as per your database schema
        values = cur.fetchall()
        print(values)
        
        cur.close()
        
        return render_template('update_form.html', columns=columns, table_name=table_name, values = values)
    
@app.route('/update-values2', methods=['GET', 'POST'])
def update_values2():
    if request.method == 'POST':
        table_name = request.form['tableName']
        # columns = request.form.getlist('columns')
        # values = request.form.getlist('values')
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM {table_name}")  # Adjust this query as per your database schema
        oldvalues = cur.fetchall()
        cur.close()
        
        values = {key: request.form[key] for key in request.form if (key != 'tableName' and key != 'whereCondition' and request.form[key]!='')}
        
        where_condition = ''
        
        
        
        if (request.form['whereCondition']!=''):
            where_condition = request.form['whereCondition']
        
        print(values)
        print(where_condition)
        
        # columns = ', '.join(values.keys())
        
        # print(columns)
        

        # Construct the SET part of the SQL query
        set_clause = ", ".join([f"{col} = %s" for col in values.keys()])
        
        print(set_clause)

        # Construct the UPDATE query
        
        sql = ''
        
        if (where_condition!=''):
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_condition}"
        else:
            sql = f"UPDATE {table_name} SET {set_clause}"
            
        print(sql)
        

        # Prepare the values for the SET clause
        set_values = values
        
        u = tuple(values.values())
        print(u)
        
        print(set_values)
        error = None
        try:
            # Execute the UPDATE query
            cur = mysql.connection.cursor()
            cur.execute(sql, u)
            mysql.connection.commit()

            flash('Update operation successful', 'success')
            # return render_template('display_table.html', table_name=table_name, columns=columns2, values=values, oldvalues=oldvalues, error = error)
        
            # return redirect(url_for('some_route'))  # Redirect to some route after successful update

        except Exception as e:
            mysql.connection.rollback()
            error = str(e)
            flash(f'Error updating values: {str(e)}', 'error')
            # return redirect(url_for('some_route'))  # Redirect to some route after error
        
        cur = mysql.connection.cursor()
        
        cur.execute(f"select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{table_name}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        columns2 = cur.fetchall()
        
        cur.execute(f"select ORDINAL_POSITION from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{table_name}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        ORDINAL_POSITION = cur.fetchall()
        
        combined = list(zip(columns2, ORDINAL_POSITION))

        # Sort the combined list based on the values in ORDINAL_POSITION
        sorted_combined = sorted(combined, key=lambda x: x[1])

        # Extract the sorted columns2 from the sorted_combined list
        columns2 = [item[0] for item in sorted_combined]
        
        cur.execute(f"SELECT * FROM {table_name}")  # Adjust this query as per your database schema
        values = cur.fetchall()
        
        oldcolumns2=columns2


        return render_template('display_table.html', table_name=table_name, columns=columns2, oldcolumns2=oldcolumns2, values=values, oldvalues=oldvalues, error = error, op='update')
        
@app.route('/delete-values', methods=['GET', 'POST'])
def delete_values():
    if request.method == 'POST':
        table_name = request.form['tableName']
        cur = mysql.connection.cursor()
        print("A")
        cur.execute(f"select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{table_name}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        columns = cur.fetchall()
        
        cur.execute(f"select ORDINAL_POSITION from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{table_name}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        ORDINAL_POSITION = cur.fetchall()
        
        combined = list(zip(columns, ORDINAL_POSITION))

        # Sort the combined list based on the values in ORDINAL_POSITION
        sorted_combined = sorted(combined, key=lambda x: x[1])

        # Extract the sorted columns from the sorted_combined list
        columns = [item[0] for item in sorted_combined]
        
        cur.execute(f"SELECT * FROM {table_name}")  # Adjust this query as per your database schema
        values = cur.fetchall()
        print(values)
        
        cur.close()
        
        return render_template('delete_form.html', columns=columns, table_name=table_name, values = values)

@app.route('/delete-values2', methods=['GET', 'POST'])
def delete_values2():
    if request.method == 'POST':
        table_name = request.form['tableName']
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM {table_name}")  # Adjust this query as per your database schema
        oldvalues = cur.fetchall()
        cur.close()
        
        where_condition = ''
        
        
        
        if (request.form['whereCondition']!=''):
            where_condition = request.form['whereCondition']
        
        print(where_condition)
        
        # Construct the UPDATE query
        
        sql = ''
        
        if (where_condition!=''):    
            sql = f"DELETE FROM {table_name} WHERE {where_condition}"
        else:
            sql = f"DELETE FROM {table_name}"
        
        print(sql)
        
        error = None
        try:
            # Execute the UPDATE query
            cur = mysql.connection.cursor()
            cur.execute(sql)
            mysql.connection.commit()

            flash('Delete operation successful', 'success')
            # return render_template('display_table.html', table_name=table_name, columns=columns2, values=values, oldvalues=oldvalues, error = error)
        
            # return redirect(url_for('some_route'))  # Redirect to some route after successful update

        except Exception as e:
            mysql.connection.rollback()
            error = str(e)
            flash(f'Error updating values: {str(e)}', 'error')
            # return redirect(url_for('some_route'))  # Redirect to some route after error
        
        cur = mysql.connection.cursor()
        
        cur.execute(f"select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{table_name}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        columns2 = cur.fetchall()
        
        cur.execute(f"select ORDINAL_POSITION from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{table_name}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        ORDINAL_POSITION = cur.fetchall()
        
        combined = list(zip(columns2, ORDINAL_POSITION))

        # Sort the combined list based on the values in ORDINAL_POSITION
        sorted_combined = sorted(combined, key=lambda x: x[1])

        # Extract the sorted columns2 from the sorted_combined list
        columns2 = [item[0] for item in sorted_combined]
        
        cur.execute(f"SELECT * FROM {table_name}")  # Adjust this query as per your database schema
        values = cur.fetchall()
        
        oldcolumns2=columns2


        return render_template('display_table.html', table_name=table_name, columns=columns2, oldcolumns2=oldcolumns2, values=values, oldvalues=oldvalues, error = error, op='update')

@app.route('/rename-table', methods=['GET', 'POST'])
def rename_table():
    if request.method == 'POST':
        table_name = request.form['tableName']
        cur = mysql.connection.cursor()
        print("A")
        cur.execute(f"select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{table_name}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        columns = cur.fetchall()
        
        cur.execute(f"select ORDINAL_POSITION from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{table_name}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        ORDINAL_POSITION = cur.fetchall()
        
        combined = list(zip(columns, ORDINAL_POSITION))

        # Sort the combined list based on the values in ORDINAL_POSITION
        sorted_combined = sorted(combined, key=lambda x: x[1])

        # Extract the sorted columns from the sorted_combined list
        columns = [item[0] for item in sorted_combined]
        
        cur.execute(f"SELECT * FROM {table_name}")  # Adjust this query as per your database schema
        values = cur.fetchall()
        print(values)
        
        cur.close()
        
        return render_template('rename_form.html', columns=columns, table_name=table_name, values= values)


@app.route('/rename-table2', methods=['GET', 'POST'])
def rename_table2():
    if request.method == 'POST':
        table_name = request.form['tableName']
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM {table_name}")  # Adjust this query as per your database schema
        
        newTableName = table_name
        
        oldvalues = cur.fetchall()
        
        cur.execute(f"select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{newTableName}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        oldcolumns2 = cur.fetchall()
        
        cur.execute(f"select ORDINAL_POSITION from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{newTableName}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        ORDINAL_POSITION = cur.fetchall()
        
        combined = list(zip(oldcolumns2, ORDINAL_POSITION))

        # Sort the combined list based on the values in ORDINAL_POSITION
        sorted_combined = sorted(combined, key=lambda x: x[1])

        # Extract the sorted oldcolumns2 from the sorted_combined list
        oldcolumns2 = [item[0] for item in sorted_combined]
        
        cur.close()
        
        
        if (request.form['newTableName']!=''): 
            newTableName = request.form['newTableName']
            
        print(newTableName)
        
        values = {key: request.form[key] for key in request.form if (key != 'newTableName' and key != 'tableName' and request.form[key]!='')}
        print(values)
        for key, value in values.items():
            cur = mysql.connection.cursor()
            sql = f"ALTER TABLE {table_name} RENAME COLUMN {key} TO {value}"
            cur.execute(sql)
            mysql.connection.commit()
        
        # Construct the UPDATE query
        error = None
    
        if (request.form['newTableName']!=''): 
            sql = f"ALTER TABLE {table_name} RENAME TO {newTableName}"
            print(sql)
            
            try:
                # Execute the UPDATE query
                cur = mysql.connection.cursor()
                cur.execute(sql)
                mysql.connection.commit()

                flash('Delete operation successful', 'success')

            except Exception as e:
                mysql.connection.rollback()
                error = str(e)
                flash(f'Error updating values: {str(e)}', 'error')
        
        cur = mysql.connection.cursor()
        
        cur.execute(f"select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{newTableName}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        columns2 = cur.fetchall()
        
        cur.execute(f"select ORDINAL_POSITION from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{newTableName}' AND TABLE_SCHEMA='transportmanagement';")  # Adjust this query as per your database schema
        ORDINAL_POSITION = cur.fetchall()
        
        combined = list(zip(columns2, ORDINAL_POSITION))

        # Sort the combined list based on the values in ORDINAL_POSITION
        sorted_combined = sorted(combined, key=lambda x: x[1])

        # Extract the sorted columns2 from the sorted_combined list
        columns2 = [item[0] for item in sorted_combined]
        
        cur.execute(f"SELECT * FROM {newTableName}")  # Adjust this query as per your database schema
        values = cur.fetchall()


        return render_template('display_table.html', newTableName = newTableName, table_name=table_name, oldcolumns2=oldcolumns2, columns=columns2, values=values, oldvalues=oldvalues, error = error, op='update')

@app.route('/custom-query', methods=['GET'])
def custom_query():
    return render_template('custom_query.html')
    
@app.route('/execute_query', methods=['POST'])
def execute_and_display():
    try:
        # conn = connect_to_database(host, user, passwd, 'transportmanagement')
        query = request.form['sql_query']
        table_name = parse_query(query)
        if (table_name == "Query is not supported"):
            return "Query is not supported"

        # table_fields = get_field_names(conn, table_name)
        table_fields = get_field_names(table_name)
        before_path = r'tmp\before.txt'
        after_path = r'tmp\after.txt'
        if (query.split()[0].lower() == 'select'):
            before_query = query
            tokens = query.split()
            if (tokens[1].lower() == '*'):
                table_fields = get_field_names(table_name)
                if (table_name.lower() == "users"):
                    table_fields.remove('user_img')
                    before_query = after_query = f"SELECT email, password, admin_priveleges, data_ from {table_name}"
                    print(table_fields)
                
            else:
                # GET the table fields from the query
                table_fields = tokens[1].split(',')
                table_fields = [field.strip() for field in table_fields]
            
            before_result = execute_query(before_query)
            if (before_result[0] == -1):
                return "ERROR IN EXECUTING QUERY --> " + str(before_result[1])
            makeASCII(before_result[1], table_fields, before_path)
            # print(before_result[1])
            py_path = sys.executable
            subprocess.run([py_path, "diff2HtmlCompare\orgTable.py", before_path, before_path], check=True) 
            return render_template('diff.html')


        if (table_name.lower() == "users"):
            table_fields.remove('user_img')
            before_query = after_query = f"SELECT email, password, admin_priveleges, data_ from {table_name}"
        else:
            before_query = after_query = f"SELECT * FROM {table_name}" 

        before_result = execute_query(before_query)
        if (before_result[0] == -1):
            return "ERROR IN EXECUTING QUERY TO FETCH STARTNG STATE OF THE TABLE --> " + str(before_result[1])
        
        makeASCII(before_result[1], table_fields, before_path)
        res = execute_query(query)

        if (res[0] == -1):
            return "ERROR IN EXECUTING QUERY --> " + str(res[1])
        
        after_result = execute_query(after_query)
        if (after_result[0] == -1):
            return "ERROR IN EXECUTING QUERY TO FETCH CHANGED STATE OF THE TABLE --> " + str(after_result[1])
        
        makeASCII(after_result[1], table_fields, after_path)
        py_path = sys.executable
        subprocess.run([py_path, "diff2HtmlCompare\diff.py", before_path, after_path], check=True) 
        # return "Query executed successfully"
        return render_template('diff.html')
    except:
        cur = mysql.connection.cursor()
        cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='transportmanagement'")  # Adjust this query as per your database schema
        table_names = cur.fetchall()
        print("WORKKKKKKK")
        print(table_names)
        cur.close()
        # return jsonify({'table_names': table_names})
        # print(j)
        return render_template('view_tables.html', table_names=table_names)

    
# Function to execute a MySQL query and return results
def execute_query(query):
    try:
        # cursor = conn.cursor()
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        # conn.commit()
        mysql.connection.commit()
        cursor.close()
        return 0,result
    except:
        return -1, "Error in executing query"
    

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
    
# Function to get field names of a table
def get_field_names(table_name):
    try:
        query = f"SHOW COLUMNS FROM {table_name}"
        # cursor = conn.cursor()
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        field_names = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return field_names
    except:
        print(f"Error getting field names")
        return None

def table_diff(before_file_path, after_file_path, diff_file_path):
    with open(before_file_path, 'r') as before_file:
        before_content = before_file.read().splitlines()
    
    with open(after_file_path, 'r') as after_file:
        after_content = after_file.read().splitlines()

    custom_html_diff = make_custom_html_diff(before_content, after_content)
    with open(diff_file_path, 'w') as diff_file:
        diff_file.write('<html><body>')
        diff_file.write(custom_html_diff)
        diff_file.write('</body></html>')


def make_custom_html_diff(before_content, after_content):
    diff = difflib.ndiff(before_content, after_content)
    
    result = []
    for line in diff:
        if line.startswith('-'):
            result.append(f'<span style="color:red; text-decoration:line-through;">{line[2:]}</span>')
        elif line.startswith('+'):
            result.append(f'<span style="color:green;">{line[2:]}</span>')
    
    return '\n'.join(result)

def makeASCII(query_result, field_names, file_path):
    if not query_result:
        query_result = [('No data',) * len(field_names)]

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
