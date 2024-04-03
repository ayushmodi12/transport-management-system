'''from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import login_config

app = Flask(__name__)

app.config['MYSQL_HOST'] = login_config.MYSQL_HOST
app.config['MYSQL_USER'] = login_config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = login_config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = login_config.MYSQL_DB

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('login_index.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        app.logger.info('Received POST request to add student: Name - %s, Email - %s', name, email)
        
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO students (name, email) VALUES (%s, %s)", (name, email))
            mysql.connection.commit()
            app.logger.info('Student added successfully: Name - %s, Email - %s', name, email)
        except Exception as e:
            app.logger.error('Error adding student to database: %s', str(e))
        finally:
            cur.close()
        
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)'''

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import login_config

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = login_config.MYSQL_HOST
app.config['MYSQL_USER'] = login_config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = login_config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = login_config.MYSQL_DB

mysql = MySQL(app)

# Routes

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')

'''@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        option = request.form['option']
        if option == 'login':
            return redirect(url_for('login'))
        elif option == 'signup':
            return redirect(url_for('signup'))
    return render_template('login_signup_index.html')'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Fetch form data
        username = request.form['username']
        password = request.form['password']

        # Cursor creation
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()

        # Close cursor
        cur.close()

        if user:
            # User found, redirect to dashboard or profile page
            flash('Login Successful', 'success')
            return redirect(url_for('landing'))  # Replace 'dashboard' with your dashboard route
        else:
            # User not found or credentials incorrect
            flash('Invalid username or password', 'error')
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
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))

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

@app.route('/booking', methods=['GET', 'POST'])
def booking():
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

    return render_template('booking.html')


if __name__ == '__main__':
    app.run(debug=True)
