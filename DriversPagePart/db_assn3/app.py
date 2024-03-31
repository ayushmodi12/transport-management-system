from flask import Flask, render_template
from sqlalchemy import text,create_engine
import json
engine = create_engine("mysql+pymysql://root:MySQL_R_Shr_Ag@localhost/TransportManagement?charset=utf8mb4")

app = Flask(__name__)

#################################################################
# This is the email entered upon login.
# replace this with the user entered value upon integration
email = 'max_verstappen@iitgn.ac.in'
#################################################################

def driver_details():
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


@app.route("/drivers")
def home_page():
    info = driver_details()
    vehicle_type, license_plate_number = vehicles_driven()
    bank=json.loads(info['bank_details'])
    ifsc = bank['ifsc_code']
    acc_no = bank['account_number']
    branch = bank['branch_name']
    return render_template('home.html', name = info['first_name']+' '+info['last_name'],number=info['phone_number'],
                           email_id = info['email_id'], join = info['date_of_joining'], license = info['driver_license_number'],
                           vehicles = vehicle_type+' '+'('+license_plate_number+')',
                           ifsc = 'IFSC Code: '+ifsc,acc='Account Number: '+acc_no,branch='Branch: '+branch)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5500,debug=True)
