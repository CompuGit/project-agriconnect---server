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

