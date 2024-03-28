from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL
from datetime import datetime
from uuid import uuid4
import yaml

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db = yaml.full_load(open('db.yaml'))

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

# Routes
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
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (username, password))
        user = cur.fetchone()

        # Close cursor
        cur.close()

        if user:
            # User found, redirect to dashboard or profile page
            flash('Login Successful', 'success')
            session['emailID'] = username
            return redirect(url_for('landing'))  # Replace 'dashboard' with your dashboard route
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
    route = route[1:]

    # if not selected_seat or not licence_plate_number:
    #     return jsonify({'error': 'No seat or licence plate number provided'}), 400

    # user_email = 'exampsfle_email@example.com'
    user_email = data.get('userEmail')
    c = route[0]
    capacity = 0
    if (c == 0):
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
    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO Booking (email_id, booking_id, booked_seat, booking_created, capacity, route, _date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (user_email, booking_id, selected_seat, date_time, capacity, route, date, ))
        mysql.connection.commit()
        return jsonify({'message': 'Booking successful'}), 200
    except Exception as e:
        mysql.connection.rollback()
        print("ACHA")
        print(e)
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()


@app.route('/fetch-booked-seats', methods=['GET', 'POST'])
def fetch_booked_seats():
    if request.method == 'POST':    
        data = request.json
        date = data.get('_date')
        route = data.get('route')
        route = route[1:]
        # user_email = data.get('userEmail')
        c = route[0]
        capacity = 0
        if (c == 0):
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
    route = route[1:]
        # user_email = data.get('userEmail')
    c = route[0]
    capacity = 0
    if (c == 0):
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
        return jsonify({'canceledSeat': canceled_seat}), 200
    except Exception as e:
        print("LOCHA")
        return jsonify({'error': str(e)}), 500


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

if __name__ == "__main__":
    app.run(debug=True)
