CREATE DATABASE if not exists TransportManagement;
use TransportManagement; 


-- TABLES 

CREATE TABLE if not exists Driver
(
  driver_license_number  varchar(16)  NOT NULL,
  email_id varchar(50) NOT NULL,
  first_name varchar(20) NOT NULL,
  last_name varchar(20),
  phone_number varchar(10) NOT NULL UNIQUE,
  date_of_joining  date,
  bank_details JSON,
  primary key (driver_license_number)
);

CREATE TABLE if not exists Faculty
(
  email_id varchar(50) NOT NULL,
  first_name varchar(20) NOT NULL,
  last_name varchar(20),
  phone_number varchar(10) NOT NULL UNIQUE,
  primary key (email_id)
);

CREATE table if not exists Vehicle
(
  license_plate_number varchar(50) NOT NULL,
  capacity  int,
  owner_first_name  varchar(20)  NOT NULL,
  owner_last_name  varchar(20)  NOT NULL,
  vehicle_type enum ('Bus', 'Car', 'Two-wheeler', 'Auto', 'Van') not null,
  primary key (license_plate_number)
);


CREATE table if not exists Students
(
  email_id varchar(50) NOT NULL,
  first_name varchar(20) NOT NULL,
  last_name varchar(20),
  phone_number varchar(10) NOT NULL UNIQUE,
  guardian_name varchar(10),
  primary key (email_id)
);

CREATE table if not exists Staff
(
  email_id varchar(50) NOT NULL,
  first_name varchar(20) NOT NULL,
  last_name varchar(20),
  phone_number varchar(10) NOT NULL UNIQUE,
  primary key(email_id)
);

CREATE table if not exists Parking_Space
(
  location  varchar(100)  NOT NULL,
  capacity  int,
  primary key (location)
);

CREATE table if not exists Shops
(
  name_of_shop  varchar(50)  NOT NULL,
  location  varchar(50)  NOT NULL,
  owner_name  varchar(20)  NOT NULL,
  primary key(name_of_shop, location)
);



CREATE table if not exists Users
(
  email  varchar(100)  NOT NULL,
  password  varchar(100)  NOT NULL UNIQUE,
  admin_priveleges enum ('yes', 'no') not null default 'no',
  data_ JSON, -- here data_ becomes the user defined data type
  user_img blob,
  primary key (email)
);

CREATE TABLE if not exists DrivenBy
(
  driver_license_number  varchar(16)  NOT NULL,
  license_plate_number  varchar(50) NOT NULL,
  primary key (driver_license_number, license_plate_number)
);

CREATE table if not exists Goods
(
  name_of_shop  varchar(50)  NOT NULL,
  location  varchar(50)  NOT NULL,
  date_and_time_of_transport date NOT NULL,
  from_ varchar(20),
  to_ varchar(20),
  primary key (name_of_shop, location)
);

CREATE table if not exists Route
(
  route_id varchar(20)  NOT NULL,
  starting_station  varchar(20)  NOT NULL,
  ending_station  varchar(50)  NOT NULL,
  start_time  time,
  estimated_travel_time  varchar(6),
  route_distance  int,
  primary key (starting_station, ending_station)
);

CREATE table if not exists Insurance
(
  insurance_id varchar(18) NOT NULL,
  license_plate_number varchar(16) NOT NULL,
  first_name varchar(20) NOT NULL,
  last_name varchar(20),
  start_date varchar(20) NOT NULL,
  end_date varchar(20) NOT NULL,
  primary key (insurance_id, license_plate_number)
);

CREATE table if not exists TransportationLog
(
  license_plate_number varchar(16) NOT NULL,
  starting_station varchar(50) NOT NULL,
  ending_station varchar(50) NOT NULL,
  time_ time,
  driver_first_name varchar(20) NOT NULL,
  driver_last_name varchar(20) NOT NULL,
  num_of_passengers int,
  entry_exit enum ('entry', 'exit') not null,
  primary key (license_plate_number, starting_station, ending_station)
);

CREATE table if not exists Booking
(
  email_id varchar(50) NOT NULL,
  booking_id varchar(50) NOT NULL,
  booked_seat varchar(50) NOT NULL,
  booking_created datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  capacity varchar(20) NOT NULL,
  route varchar(100)  NOT NULL,
  _date varchar(20)  NOT NULL,
  primary key (booking_id)
);


-- CREATE table if not exists Seats
-- (
--   bus_license_plate_number  varchar(16)  NOT NULL,
--   seats_booked varchar(16)  DEFAULT NULL,
--   booking_created datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   primary key (bus_license_plate_number, booking_created)
-- );

CREATE table if not exists ShopVehicles
(
  name_of_shop  varchar(50)  NOT NULL,
  location  varchar(50)  NOT NULL,
  license_plate_number  varchar(16) NOT NULL,
  primary key (name_of_shop, location, license_plate_number)
);

CREATE table if not exists PrivateOwnership
(
  license_plate_number varchar(10)  NOT NULL,
  email_id varchar(50) NOT NULL,
  primary key (license_plate_number)
);

CREATE table if not exists AllocatedParking
(
  license_plate_number varchar(16) NOT NULL,
  location  varchar(100)  NOT NULL,
  primary key (license_plate_number)
);

CREATE table if not exists GoodsTransported
(
  license_plate_number varchar(16) NOT NULL,
  to_ varchar(20),
  from_ varchar(20),
  primary key (license_plate_number)
);


-- Indexes are needed to be added because a table has only that many number of indexes as the number of foreign keys, So to reference we need to add more index.


ALTER TABLE shops ADD INDEX location_index (location); 

ALTER TABLE DRIVENBY
ADD CONSTRAINT drive_by_f1
foreign key (driver_license_number) references Driver(driver_license_number);


ALTER TABLE DRIVENBY
ADD CONSTRAINT drive_by_f2
foreign key (license_plate_number) references Vehicle(license_plate_number);

ALTER TABLE Goods
ADD CONSTRAINT Goods_f1
foreign key (name_of_shop) references shops(name_of_shop);

ALTER TABLE Goods
ADD CONSTRAINT Goods_f2
foreign key (location) references shops(location);


ALTER TABLE Insurance
ADD CONSTRAINT Insurance_f1
foreign key (license_plate_number) references Vehicle(license_plate_number);

ALTER TABLE TransportationLog
ADD CONSTRAINT TransLog_f1
foreign key(license_plate_number) references Vehicle(license_plate_number);

ALTER TABLE TransportationLog
ADD CONSTRAINT TransLog_f2
foreign key(starting_station) references Route(starting_station);

ALTER TABLE Route ADD INDEX ending_stat_index (ending_station);

ALTER TABLE TransportationLog
ADD CONSTRAINT TransLog_f3
foreign key(ending_station) references Route(ending_station);

ALTER TABLE ShopVehicles
ADD CONSTRAINT SV_f1
foreign key (name_of_shop) references shops(name_of_shop);

ALTER TABLE ShopVehicles
ADD CONSTRAINT SV_f2
foreign key (location) references shops(location);

ALTER TABLE ShopVehicles
ADD CONSTRAINT SV_f3
foreign key (license_plate_number) references Vehicle(license_plate_number);

ALTER TABLE PrivateOwnership
ADD CONSTRAINT POwner_f1
foreign key (email_id) references Staff(email_id);

ALTER TABLE AllocatedParking
ADD CONSTRAINT AllotPark_f1
foreign key (license_plate_number) references Vehicle(license_plate_number);

ALTER TABLE AllocatedParking
ADD CONSTRAINT AllotPark_f2
foreign key (location) references Parking_Space(location);

ALTER TABLE GoodsTransported
ADD CONSTRAINT GTrans_f1
foreign key (license_plate_number) references Vehicle(license_plate_number);


INSERT INTO Driver VALUES
('1234567890123456', 'kumaramit@iitgn.ac.in', 'Amit', 'Kumar', '9876543210', '2017-01-05', '{"account_number":"1234567890534647","ifsc_code":"1456239875487890","branch_name":"Bangalore"}'),
('2345678901234567', 'john_doe@iitgn.ac.in', 'John', 'Doe', '8765432109', '2018-02-15', '{"account_number":"2345678900534647","ifsc_code":"2345678905487890","branch_name":"New York"}'),
('3456789012345678', 'max_verstappen@iitgn.ac.in', 'Max', 'Verstappen', '7654321098', '2019-03-25', '{"account_number":"3456789010534647","ifsc_code":"3456789015487890","branch_name":"Los Angeles"}'),
('4567890123456789', 'koramassey@iitgn.ac.in', 'Kora', 'Massey', '6543210987', '2020-04-10', '{"account_number":"4567890120534647","ifsc_code":"4567890125487890","branch_name":"Chicago"}'),
('5678901234567890', 'emily_brown@iitgn.ac.in', 'Emily', 'Brown', '5432109876', '2021-05-20', '{"account_number":"5678901230534647","ifsc_code":"5678901235487890","branch_name":"Houston"}'),
('6789012345678901', 'bryson_greene@iitgn.ac.in', 'Bryson', 'Greene', '4321098765', '2022-06-30', '{"account_number":"6789012340534647","ifsc_code":"6789012345487890","branch_name":"San Francisco"}'),
('7890123456789012', 'briana_kirk@iitgn.ac.in', 'Briana', 'Kirk', '3210987654', '2018-02-15', '{"account_number":"7890123450534647","ifsc_code":"7890123455487890","branch_name":"New York"}'),
('8901234567890123', 'daniel_wilson@iitgn.ac.in', 'Daniel', 'Wilson', '2109876543', '2019-03-25', '{"account_number":"8901234560534647","ifsc_code":"8901234565487890","branch_name":"Los Angeles"}'),
('9012345678901234', 'olivia_anderson@iitgn.ac.in', 'Olivia', 'Anderson', '1234567890', '2020-04-10', '{"account_number":"9012345670534647","ifsc_code":"9012345675487890","branch_name":"Chicago"}'),
('0123456789012345', 'sophia_taylor@iitgn.ac.in', 'Sophia', 'Taylor', '2345678901', '2021-05-20','{"account_number":"0123456780534647","ifsc_code":"0123456785487890","branch_name":"Houston"}');


-- To query data from the UDDT
-- SELECT JSON_EXTRACT(bank_details, '$.account_number') AS Account_Number,
--        JSON_EXTRACT(bank_details, '$.ifsc_code') AS IFSC_Code,
--        JSON_EXTRACT(bank_details, '$.branch_name') AS Branch_Name
-- FROM Driver;


INSERT INTO Faculty VALUES 
('faculty_A@iitgn.ac.in', 'First_A', 'Last_A', '9876543211'),
('faculty_B@iitgn.ac.in', 'First_B', 'Last_B', '8765432110'),
('faculty_C@iitgn.ac.in', 'First_C', 'Last_C', '7654321109'),
('faculty_D@iitgn.ac.in', 'First_D', 'Last_D', '6543211098'),
('faculty_E@iitgn.ac.in', 'First_E', 'Last_E', '5432109875'),
('faculty_F@iitgn.ac.in', 'First_F', 'Last_F', '4321098764'),
('faculty_G@iitgn.ac.in', 'First_G', 'Last_G', '3210987653'),
('faculty_H@iitgn.ac.in', 'First_H', 'Last_H', '2109876542'),
('faculty_I@iitgn.ac.in', 'First_I', 'Last_I', '1098765432'),
('faculty_J@iitgn.ac.in', 'First_J', 'Last_J', '2345678901');


INSERT INTO Vehicle VALUES 
('GJ01AB1234', 4, 'Kora', 'Massey', 'Car'),
('GJ02CD4567', 7, 'Donald', 'Davila', 'Two-wheeler'),
('GJ03EF7890', 5, 'Rayne', 'Romero', 'Car'),
('GJ04GH0123', 6, 'Bryson', 'Greene', 'Van'),
('GJ05IJ4567', 4, 'Selena', 'Wood', 'Car'),
('GJ06KL7890', 8, 'Carson', 'Conner', 'Van'),
('RJ07MN0123', 5, 'Alondra', 'Bell', 'Car'),
('RJ08OP3456', 7, 'Emmett', 'Hood', 'Two-wheeler'),
('GJ09QR6789', 4, 'Briana', 'Kirk', 'Bus'),
('GJ10ST0123', 6, 'Alessandro', 'Carso', 'Van'),
('RJ07MN0245', 35, 'Max', 'Verstappen', 'Bus'),
('GJ09QT6969', 35, 'Lewis', 'Hamilton', 'Bus');

-- INSERT INTO Booking(license_plate_number, email_id, booking_id, booked_seat, booking_created, route_id) VALUES
-- ('RJ07MN0245','studentA@iitgn.ac.in', '001', '1', '2021-10-16 22:15:13', '1'),
-- ('RJ07MN0245','studentB@iitgn.ac.in', '002', '5', '2021-10-17 23:15:13', '4'),
-- ('RJ07MN0245','studentD@iitgn.ac.in', '003', '9', '2021-10-19 05:15:13', '2');

-- INSERT INTO Seats(bus_license_plate_number, seats_booked, booking_created) VALUES
-- ('GJ09QR6789', NULL, '2021-10-17 20:15:13'),
-- ('RJ07MN0245', '3', '2021-10-17 23:15:13'),
-- ('GJ09QT6969', '2,9,6,5', '2021-10-17 23:15:13');


INSERT INTO Students (email_id, first_name, last_name, phone_number, guardian_name)
VALUES 
('studentA@iitgn.ac.in', 'Stu_First_A', 'Stu_Last_A', '9876543220', 'Gua_Last_A'),
('studentB@iitgn.ac.in', 'Stu_First_B', 'Stu_Last_B', '8765432119', 'Gua_Last_B'),
('studentC@iitgn.ac.in', 'Stu_First_C', 'Stu_Last_C', '7654321108', 'Gua_Last_C'),
('studentD@iitgn.ac.in', 'Stu_First_D', 'Stu_Last_D', '6543210997', 'Gua_Last_D'),
('studentE@iitgn.ac.in', 'Stu_First_E', 'Stu_Last_E', '5432109886', 'Gua_Last_E'),
('studentF@iitgn.ac.in', 'Stu_First_F', 'Stu_Last_F', '4321098775', 'Gua_Last_F'),
('studentG@iitgn.ac.in', 'Stu_First_G', 'Stu_Last_G', '3210987664', 'Gua_Last_G'),
('studentH@iitgn.ac.in', 'Stu_First_H', 'Stu_Last_H', '2109876553', 'Gua_Last_H'),
('studentI@iitgn.ac.in', 'Stu_First_I', 'Stu_Last_I', '1098765442', 'Gua_Last_I'),
('studentJ@iitgn.ac.in', 'Stu_First_J', 'Stu_Last_J', '2345678910', 'Gua_Last_J');


INSERT INTO Staff (email_id, first_name, last_name, phone_number)
VALUES 
('staffA@iitgn.ac.in', 'Staff_First_A', 'Staff_Last_A', '9876543201'),
('staffB@iitgn.ac.in', 'Staff_First_B', 'Staff_Last_B', '8765432102'),
('staffC@iitgn.ac.in', 'Staff_First_C', 'Staff_Last_C', '7654321093'),
('staffD@iitgn.ac.in', 'Staff_First_D', 'Staff_Last_D', '6543210984'),
('staffE@iitgn.ac.in', 'Staff_First_E', 'Staff_Last_E', '5432109875'),
('staffF@iitgn.ac.in', 'Staff_First_F', 'Staff_Last_F', '4321098766'),
('staffG@iitgn.ac.in', 'Staff_First_G', 'Staff_Last_G', '3210987657'),
('staffH@iitgn.ac.in', 'Staff_First_H', 'Staff_Last_H', '2109876548'),
('staffI@iitgn.ac.in', 'Staff_First_I', 'Staff_Last_I', '1098765439'),
('staffJ@iitgn.ac.in', 'Staff_First_J', 'Staff_Last_J', '2345678901');


INSERT INTO Parking_Space (location, capacity) VALUES 
('Housing Block Parking Area', 50),
('Hostel Parking Area', 50),
('Behind Academic Block', 4),
('Academic Block Parking lot', 50);

INSERT INTO Shops (name_of_shop, location, owner_name) VALUES
('Amul','Duven Hostel', 'Owner1'),
('Krupa Generals','Duven Hostel','Owner2'),
('JK Grocery','Firpeal Hostel','Owner3'),
('VS FastFood','Hiqom Hostel','Owner4'),
('Fruit Shop', 'Central Arcade', 'Owner5'),
('2 Degree', 'AB 1', 'Owner6'),
('Stationary Shop','Central Arcade', 'Owner7'),
('Juice Shop','Sports Complex','Owner8');


INSERT INTO DrivenBy (driver_license_number, license_plate_number) VALUES
('1234567890123456', 'GJ01AB1234'),
('2345678901234567', 'GJ02CD4567'),
('3456789012345678', 'GJ03EF7890'),
('4567890123456789', 'GJ04GH0123'),
('5678901234567890', 'GJ05IJ4567'),
('6789012345678901', 'GJ06KL7890'),
('7890123456789012', 'RJ07MN0123'),
('8901234567890123', 'RJ08OP3456'),
('9012345678901234', 'GJ09QR6789'),
('0123456789012345', 'GJ10ST0123');


Insert into Goods (name_of_shop, location, date_and_time_of_transport, from_, to_) values 
('Amul','Duven Hostel','2023-11-02','Ahmedabad','ITTGN Campus'),
('Krupa Generals','Duven Hostel','2023-12-01','Palaj','IITGN Campus'),
('JK Grocery','Firpeal Hostel','2024-01-02','Vadodara','IITGN Campus'),
('VS FastFood','Hiqom Hostel','2024-01-03','Ahmedabad','IITGN Campus'),
('Fruit Shop','Central Arcade','2024-02-09','Ahmedabad','IITGN Campus'),
('2 Degree','AB 1','2024-02-10','Ankleshwar','IITGN Campus'),
('Stationary Shop','Central Arcade','2024-02-11','IITGN Campus','Palaj'),
('Juice Shop','Sports Complex','2024-02-12','Nadiad','IITGN Campus');

INSERT INTO Route (route_id, starting_station, ending_station, start_time, estimated_travel_time, route_distance)
VALUES 
  ('1', 'IITGN Campus', 'Ahmedabad Railway Station', '17:00:00', '1h30m', 10),
  ('2', 'Kudasan', 'IITGN Campus', '21:00:00', '30m', 5),
  ('3', 'IITGN Campus', 'Gandhinagar Bus Stand', '16:30:00', '45m', 8),
  ('4', 'Visat Circle', 'IITGN Campus', '20:00:00', '45m', 7),
  ('5', 'IITGN Campus', 'Ahmedabad Airport', '18:00:00', '1h', 9),
  ('6', 'IITGN Campus', 'Kudasan', '20:00:00', '30m', 5),
  ('7', 'IITGN Campus', 'Sargasan', '19:00:00', '40m', 6),
  ('8', 'Sargasan', 'IITGN Campus', '22:00:00', '40m', 6),
  ('9', 'IITGN Campus', 'Visat Circle', '19:45:00', '45m', 7);


INSERT INTO Insurance (insurance_id, license_plate_number, first_name, last_name, start_date, end_date)
VALUES 
('INS123456789', 'GJ01AB1234', 'John', 'Doe', '2024-01-01', DATE_ADD('2024-01-01', INTERVAL 5 YEAR)),
('INS234567890', 'GJ02CD4567', 'Alice', 'Smith', '2024-02-01', DATE_ADD('2024-02-01', INTERVAL 3 YEAR)),
('INS345678901', 'GJ03EF7890', 'Michael', 'Johnson', '2024-03-01', DATE_ADD('2024-03-01', INTERVAL 5 YEAR)),
('INS456789012', 'GJ04GH0123', 'Emily', 'Brown', '2024-04-01', DATE_ADD('2024-04-01', INTERVAL 3 YEAR)),
('INS567890123', 'GJ05IJ4567', 'David', 'Martinez', '2024-05-01', DATE_ADD('2024-05-01', INTERVAL 3 YEAR)),
('INS678901234', 'GJ06KL7890', 'Jessica', 'Garcia', '2024-06-01', DATE_ADD('2024-06-01', INTERVAL 5 YEAR)),
('INS789012345', 'RJ07MN0123', 'Daniel', 'Wilson', '2024-07-01', DATE_ADD('2024-07-01', INTERVAL 5 YEAR)),
('INS890123456', 'RJ08OP3456', 'Olivia', 'Anderson', '2024-08-01', DATE_ADD('2024-08-01', INTERVAL 3 YEAR)),
('INS901234567', 'GJ09QR6789', 'Sophia', 'Taylor', '2024-09-01', DATE_ADD('2024-09-01', INTERVAL 5 YEAR)),
('INS012345678', 'GJ10ST0123', 'Alessandro', 'Carso', '2024-10-01', DATE_ADD('2024-10-01', INTERVAL 3 YEAR)),
('INS123456789', 'RJ07MN0245', 'Max', 'Verstappen', '2024-11-01', DATE_ADD('2024-11-01', INTERVAL 5 YEAR)),
('INS234567890', 'GJ09QT6969', 'Lewis', 'Hamilton', '2024-12-01', DATE_ADD('2024-12-01', INTERVAL 3 YEAR));


INSERT INTO ShopVehicles (name_of_shop, location, license_plate_number)
VALUES 
('Amul', 'Duven Hostel', 'GJ01AB1234'),
('Krupa Generals', 'Duven Hostel', 'GJ02CD4567'),
('JK Grocery', 'Firpeal Hostel', 'GJ03EF7890'),
('VS FastFood', 'Hiqom Hostel', 'GJ04GH0123'),
('Fruit Shop', 'Central Arcade', 'GJ05IJ4567'),
('2 Degree', 'AB 1', 'GJ06KL7890'),
('JK Grocery', 'Firpeal Hostel', 'RJ07MN0123'),
('VS FastFood', 'Hiqom Hostel', 'RJ08OP3456'),
('JK Grocery', 'Firpeal Hostel', 'GJ09QR6789'),
('VS FastFood', 'Hiqom Hostel', 'GJ10ST0123'),
('Fruit Shop', 'Central Arcade', 'RJ07MN0245'),
('2 Degree', 'AB 1', 'GJ09QT6969');



INSERT INTO PrivateOwnership (license_plate_number, email_id) VALUES
('GJ01AB1234', 'staffA@iitgn.ac.in'),
('GJ02CD4567', 'staffB@iitgn.ac.in'),
('GJ03EF7890', 'staffC@iitgn.ac.in'),
('GJ04GH0123', 'staffD@iitgn.ac.in'),
('GJ05IJ4567', 'staffE@iitgn.ac.in'),
('GJ06KL7890', 'staffF@iitgn.ac.in'),
('RJ07MN0123', 'staffG@iitgn.ac.in'),
('RJ08OP3456', 'staffH@iitgn.ac.in'),
('GJ09QR6789', 'staffI@iitgn.ac.in'),
('GJ10ST0123', 'staffJ@iitgn.ac.in');


INSERT INTO AllocatedParking (license_plate_number, location) VALUES
('GJ01AB1234', 'Housing Block Parking Area'),
('GJ02CD4567', 'Hostel Parking Area'),
('GJ03EF7890', 'Behind Academic Block'),
('GJ04GH0123', 'Academic Block Parking lot'),
('GJ05IJ4567', 'Housing Block Parking Area'),
('GJ06KL7890', 'Hostel Parking Area'),
('RJ07MN0123', 'Behind Academic Block'),
('RJ08OP3456', 'Academic Block Parking lot'),
('GJ09QR6789', 'Housing Block Parking Area'),
('GJ10ST0123', 'Hostel Parking Area');

INSERT INTO GoodsTransported (license_plate_number, to_, from_)
VALUES
('GJ01AB1234', 'ITTGN Campus', 'Ahmedabad'),
('GJ02CD4567', 'IITGN Campus', 'Palaj'),
('GJ03EF7890', 'IITGN Campus', 'Vadodara'),
('GJ04GH0123', 'IITGN Campus', 'Ahmedabad'),
('GJ05IJ4567', 'IITGN Campus', 'Ahmedabad'),
('GJ06KL7890', 'IITGN Campus', 'Ankleshwar'),
('RJ07MN0123', 'IITGN Campus', 'Vadodara'),
('RJ08OP3456', 'Palaj', 'IITGN Campus'),
('GJ09QR6789', 'IITGN Campus', 'Nadiad'),
('GJ10ST0123', 'IITGN Campus', 'Ankleshwar');


-- Insert entries from Faculty table
-- INSERT INTO Users (username, password, data_, user_img) VALUES
-- ('First_A', MD5('First_A@123'), '{"first_name": "First_A", "last_name": "Last_A", "email_id": "faculty_A@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('First_B', MD5('First_B@123'), '{"first_name": "First_B", "last_name": "Last_B", "email_id": "faculty_B@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('First_C', MD5('First_C@123'), '{"first_name": "First_C", "last_name": "Last_C", "email_id": "faculty_C@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('First_D', MD5('First_D@123'), '{"first_name": "First_D", "last_name": "Last_D", "email_id": "faculty_D@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('First_E', MD5('First_E@123'), '{"first_name": "First_E", "last_name": "Last_E", "email_id": "faculty_E@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('First_F', MD5('First_F@123'), '{"first_name": "First_F", "last_name": "Last_F", "email_id": "faculty_F@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('First_G', MD5('First_G@123'), '{"first_name": "First_G", "last_name": "Last_G", "email_id": "faculty_G@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('First_H', MD5('First_H@123'), '{"first_name": "First_H", "last_name": "Last_H", "email_id": "faculty_H@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('First_I', MD5('First_I@123'), '{"first_name": "First_I", "last_name": "Last_I", "email_id": "faculty_I@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('First_J', MD5('First_J@123'), '{"first_name": "First_J", "last_name": "Last_J", "email_id": "faculty_J@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png"));


-- Insert entries from Students table
-- INSERT INTO Users (username, password, data_, user_img) VALUES
-- ('Stu_First_A', MD5('Stu_First_A@123'), '{"first_name": "Stu_First_A", "last_name": "Stu_Last_A", "email_id": "studentA@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('Stu_First_B', MD5('Stu_First_B@123'), '{"first_name": "Stu_First_B", "last_name": "Stu_Last_B", "email_id": "studentB@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('Stu_First_C', MD5('Stu_First_C@123'), '{"first_name": "Stu_First_C", "last_name": "Stu_Last_C", "email_id": "studentC@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('Stu_First_D', MD5('Stu_First_D@123'), '{"first_name": "Stu_First_D", "last_name": "Stu_Last_D", "email_id": "studentD@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('Stu_First_E', MD5('Stu_First_E@123'), '{"first_name": "Stu_First_E", "last_name": "Stu_Last_E", "email_id": "studentE@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('Stu_First_F', MD5('Stu_First_F@123'), '{"first_name": "Stu_First_F", "last_name": "Stu_Last_F", "email_id": "studentF@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('Stu_First_G', MD5('Stu_First_G@123'), '{"first_name": "Stu_First_G", "last_name": "Stu_Last_G", "email_id": "studentG@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('Stu_First_H', MD5('Stu_First_H@123'), '{"first_name": "Stu_First_H", "last_name": "Stu_Last_H", "email_id": "studentH@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('Stu_First_I', MD5('Stu_First_I@123'), '{"first_name": "Stu_First_I", "last_name": "Stu_Last_I", "email_id": "studentI@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('Stu_First_J', MD5('Stu_First_J@123'), '{"first_name": "Stu_First_J", "last_name": "Stu_Last_J", "email_id": "studentJ@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png"));


-- Insert entries from Driver table
INSERT INTO Users (email, password, admin_priveleges, data_, user_img) VALUES
('kumaramit@iitgn.ac.in', MD5('Amit@123'), 'yes', '{"first_name": "Amit", "last_name": "Kumar", "driver_license_number": "1234567890123456"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png"));

INSERT INTO Users (email, password, data_, user_img) VALUES
('john_doe@iitgn.ac.in', MD5('John@123'), '{"first_name": "John", "last_name": "Doe", "driver_license_number": "2345678901234567"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
('max_verstappen@iitgn.ac.in', MD5('Alice@123'), '{"first_name": "Max", "last_name": "Verstappen", "driver_license_number": "3456789012345678"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
('koramassey@iitgn.ac.in', MD5('Michael@123'), '{"first_name": "Kora", "last_name": "Massey", "driver_license_number": "4567890123456789"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
('emily_brown@iitgn.ac.in', MD5('Emily@123'), '{"first_name": "Emily", "last_name": "Brown", "driver_license_number": "5678901234567890"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
('bryson_greene@iitgn.ac.in', MD5('David@123'), '{"first_name": "Bryson", "last_name": "Greene", "driver_license_number": "6789012345678901"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
('briana_kirk@iitgn.ac.in', MD5('Jessica@123'), '{"first_name": "Briana", "last_name": "Kirk", "driver_license_number": "7890123456789012"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
('daniel_wilson@iitgn.ac.in', MD5('Daniel@123'), '{"first_name": "Daniel", "last_name": "Wilson", "driver_license_number": "8901234567890123"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
('olivia_anderson@iitgn.ac.in', MD5('Olivia@123'), '{"first_name": "Olivia", "last_name": "Anderson", "driver_license_number": "9012345678901234"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
('sophia_taylor@iitgn.ac.in', MD5('Sophia@123'), '{"first_name": "Sophia", "last_name": "Taylor", "driver_license_number": "0123456789012345"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png"));


-- Insert entries from Staff table
-- INSERT INTO Users (username, password, data_, user_img) VALUES
-- ('Staff_First_A', MD5('Staff_First_A@123'), '{"first_name": "Staff_First_A", "last_name": "Staff_Last_A", "email_id": "staffA@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- ('Staff_First_B', MD5('Staff_First_B@123'), '{"first_name": "Staff_First_B", "last_name": "Staff_Last_B", "email_id": "staffB@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png")),
-- Staff_First_C, MD5('Staff_First_C@123'), '{"first_name": "Staff_First_C", "last_name": "Staff_Last_C", "email_id": "staffC@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png"),
-- Staff_First_D, MD5('Staff_First_D@123'), '{"first_name": "Staff_First_D", "last_name": "Staff_Last_D", "email_id": "staffD@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png"),
-- Staff_First_E, MD5('Staff_First_E@123'), '{"first_name": "Staff_First_E", "last_name": "Staff_Last_E", "email_id": "staffE@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png"),
-- Staff_First_F, MD5('Staff_First_F@123'), '{"first_name": "Staff_First_F", "last_name": "Staff_Last_F", "email_id": "staffF@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png"),
-- Staff_First_G, MD5('Staff_First_G@123'), '{"first_name": "Staff_First_G", "last_name": "Staff_Last_G", "email_id": "staffG@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png"),
-- Staff_First_H, MD5('Staff_First_H@123'), '{"first_name": "Staff_First_H", "last_name": "Staff_Last_H", "email_id": "staffH@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png"),
-- Staff_First_I, MD5('Staff_First_I@123'), '{"first_name": "Staff_First_I", "last_name": "Staff_Last_I", "email_id": "staffI@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png"),
-- Staff_First_J, MD5('Staff_First_J@123'), '{"first_name": "Staff_First_J", "last_name": "Staff_Last_J", "email_id": "staffJ@iitgn.ac.in"}', load_file("D:\Books & Assignments 3rdYear\Sem6\DBMS\Assignment2\icons8-male-user-material-rounded\icons8-male-user-96.png"),

-- To query data from the UDDT
-- SELECT JSON_EXTRACT(data_, '$.first_name') AS First_Name,
--          JSON_EXTRACT(data_, '$.last_name') AS Last_Name,
--          CASE
--              WHEN JSON_CONTAINS_PATH(data_,'one','$.email_id') THEN JSON_EXTRACT(data_, '$.email_id')
--              WHEN JSON_CONTAINS_PATH(data_,'one','$.driver_license_number') THEN JSON_EXTRACT(data_, '$.driver_license_number')
--          END AS Identifier
-- FROM Users;

-- Insert entries into TransportationLog
INSERT INTO TransportationLog
VALUES 
('GJ01AB1234', 'IITGN Campus', 'Ahmedabad Railway Station', '08:00:00', 'Amit','Kumar', 25, 'exit'),
('GJ02CD4567', 'Kudasan', 'IITGN Campus', '12:00:00', 'John','Doe', 20, 'entry'),
('GJ03EF7890', 'IITGN Campus', 'Gandhinagar Bus Stand', '15:00:00', 'Emily', 'Brown', 10, 'exit'),
('GJ04GH0123', 'Visat Circle', 'IITGN Campus', '07:00:00','Amit','Kumar', 15, 'entry'),
('GJ05IJ4567', 'IITGN Campus', 'Ahmedabad Airport', '10:30:00', 'David','Martinez', 5, 'exit'),
('GJ06KL7890', 'IITGN Campus', 'Gandhinagar Bus Stand', '13:00:00', 'John','Doe',  30, 'exit'),
('RJ07MN0123', 'Visat Circle', 'IITGN Campus', '08:45:00', 'Daniel','Wilson', 12, 'entry'),
('RJ07MN0123', 'IITGN Campus', 'Ahmedabad Airport', '09:45:00', 'Jessica','Garcia', 12, 'exit'),
('RJ08OP3456', 'IITGN Campus', 'Ahmedabad Airport', '11:30:00', 'Michael','Johnson', 8, 'exit'),
('GJ09QR6789', 'IITGN Campus', 'Ahmedabad Airport', '14:00:00', 'Sophia', 'Taylor',  18, 'exit');

-- Before adding index on username in the Users table
CREATE INDEX user_index
 on Users (email);

create index booking_index on booking(email_id);
create index translog_index on transportationlog(license_plate_number);
