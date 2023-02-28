CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY,
    c_fullname TEXT,
    c_phone TEXT,
    survey_no INTEGER,
    message TEXT,
    rbk_user TEXT,
    status TEXT);


CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    _username TEXT,
    phone TEXT,
    password TEXT,
    user_type TEXT);

/*SELECT * FROM users*/

INSERT INTO users (_username, phone, password, user_type)
VALUES('poorna','9876543210', '123456','farmer');

INSERT INTO users (_username, phone, password, user_type)
VALUES('venkat','9988776655', '123456','farmer');

INSERT INTO users (_username, phone, password, user_type)
VALUES('sai','9998887776', '123456','rbk');

INSERT INTO users (_username, phone, password, user_type)
VALUES('jeswanth','9999888877', '123456','transport');

INSERT INTO users (_username, phone, password, user_type)
VALUES('tharun','9999988888', '123456','ricemill');



CREATE TABLE IF NOT EXISTS farmers (
    id INTEGER PRIMARY KEY,
    _username TEXT,
    fullname TEXT,
    phone TEXT,
    bank_ac TEXT,
    aadhaar_no TEXT,
    address TEXT,
    mandal TEXT,
    village TEXT);

INSERT INTO farmers (_username, fullname, phone, bank_ac, aadhaar_no, address, mandal, village)
VALUES('poorna', 'Poorna Venkata Sai L', '9876543210', '000987654321', '0987-6543-1234', '1-121, chilakalpudi, machilipatnam', 'bandar', 'chilakalapudi');

INSERT INTO farmers (_username, fullname, phone, bank_ac, aadhaar_no, address, mandal, village)
VALUES('venkat', 'Poorna Venkata Sai L', '9988776655', '000987654321', '0987-6543-1234', '1-121, chilakalpudi, machilipatnam', 'bandar', 'chilakalapudi');



CREATE TABLE IF NOT EXISTS surveys (
    id INTEGER PRIMARY KEY,
    _username TEXT,
    phone TEXT,
    survey_no TEXT,
    land_capacity TEXT,
    land_passbook TEXT);


INSERT INTO surveys (_username, phone, survey_no, land_capacity, land_passbook)
VALUES('poorna','9876543210','123', '54321', '00098765');

INSERT INTO surveys (_username, phone, survey_no, land_capacity, land_passbook)
VALUES('poorna','9876543210','456', '55555', '00054321');

INSERT INTO surveys (_username, phone, survey_no, land_capacity, land_passbook)
VALUES('venkat','9988776655','789', '44444', '00076543');



CREATE TABLE IF NOT EXISTS crops_queue (
    crop_id INTEGER PRIMARY KEY,
    survey_no TEXT,
    crop_type TEXT,
    cut_date TEXT,
    qc_date TEXT,
    sell_date TEXT,
    bags TEXT,
    amount TEXT,
    status TEXT);

INSERT INTO crops_queue (crop_id, survey_no, crop_type, cut_date, qc_date, sell_date, bags, amount, status)
VALUES(9876, '456', 'paddy', '21-01-2023', '31-01-2023', '14-02-2023', 28, 19000, 'completed');

INSERT INTO crops_queue (crop_id, survey_no, crop_type, cut_date, qc_date, bags, status)
VALUES(9898, '123','rice', '21-01-2023', '31-01-2023', 30, 'processing'); 



CREATE TABLE IF NOT EXISTS transport_owners (
    id INTEGER PRIMARY KEY,
    _username TEXT,
    fullname TEXT,
    phone TEXT,
    address TEXT,
    mandal TEXT,
    village TEXT,
    vehicle_type TEXT,
    vehicle_no TEXT,
    vehicle_rec TEXT,
    available_dates TEXT);

INSERT INTO transport_owners (_username, fullname, phone, address, mandal, village, vehicle_type, vehicle_no, vehicle_rec, available_dates)
VALUES('jeswanth', 'Jeswanth M', '9999888877', '1-121, chilakalpudi, machilipatnam', 'bandar', 'chilakalapudi', 'Tractor', 'AP 16 AZ 1234', 'Not provided yet', '["2023-02-28","2023-03-05"]');


CREATE TABLE IF NOT EXISTS transport_queue (
    track_id INTEGER PRIMARY KEY,
    crop_id INTEGER,
    c_fullname TEXT,
    c_phone TEXT,
    d_fullname TEXT,
    d_phone TEXT,
    date_booked TEXT,
    time_slot TEXT,
    from_ TEXT,
    to_ TEXT,
    vehicle_type TEXT,
    vehicle_no TEXT,
    status TEXT);

INSERT INTO transport_queue (track_id, crop_id, c_fullname, c_phone, d_fullname, d_phone, date_booked, time_slot, from_, to_, vehicle_type, vehicle_no, status)
VALUES(300104, 9898, 'Poorna Venkata Sai L', '9876543210', 'Jeswanth M', '9999888877', '2023-03-05', '5:30 PM', '1-121, chilakalpudi, machilipatnam', 'ABC Mill MTM', 'Tractor', 'AP 16 AZ 1234', 'pending' );




CREATE TABLE IF NOT EXISTS ricemill_owners (
    id INTEGER PRIMARY KEY,
    fullname TEXT,
    millname TEXT,
    mill_phone TEXT,
    address TEXT,
    mandal TEXT,
    village TEXT,
    storage_capacity INTEGER,
    milling_capacity INTEGER,
    dispatched_bags INTEGER);


INSERT INTO ricemill_owners (fullname, millname, mill_phone, address, mandal, village, storage_capacity, milling_capacity, dispatched_bags)
VALUES( 'Tharun Narasimha M', 'ABC Rice Mill', '9999988888', '1-121, chilakalpudi, machilipatnam', 'bandar', 'chilakalapudi', 500, 500, 0);


CREATE TABLE IF NOT EXISTS ricemill_queue (
    id INTEGER PRIMARY KEY,
    millname TEXT,
    mill_phone TEXT,

    crop_id INTEGER,
    survey_no INTEGER,
    crop_get_date TEXT,
    c_fullname TEXT,
    c_phone TEXT,
    no_of_bags INTEGER,
    bags_status TEXT,

    track_id INTEGER,
    t_fullname TEXT,
    t_phone TEXT,
    vehicle_type TEXT,
    vehicle_no TEXT);

INSERT INTO ricemill_queue (millname, mill_phone, crop_id, survey_no, crop_get_date, c_fullname, c_phone, no_of_bags, bags_status, track_id, t_fullname, t_phone, vehicle_type, vehicle_no)
VALUES('ABC Rice Mill', '9999988888', 9898, 123, '2023-03-05',  'Poorna Venkata Sai L', '9876543210', 28, '', 300104, 'Jeswanth M', '9999888877', 'Tractor', 'AP 16 AZ 1234' );