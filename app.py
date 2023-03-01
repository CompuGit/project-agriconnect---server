import sqlite3
from functools import wraps
from flask import Flask, g, request, session, redirect, url_for, jsonify, render_template

app = Flask(__name__)
app.secret_key = 'my_secret_key'
app.config['DATABASE'] = './database.db'


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()


def login_required(func):
    @wraps(func)
    def wraper(*args,**kwargs):
        if session.get('logged_in'):
            return func(*args, **kwargs)
        else:
            return redirect('/login')
    return wraper


#default route
@app.route('/')
@login_required
def index():
    active_user = session.get('active_user')
    if active_user['user_type']=='farmer': return redirect('/farmer_index')
    if active_user['user_type']=='transport': return redirect('/transport_index')
    if active_user['user_type']=='ricemill': return redirect('/ricemill_index')
    if active_user['user_type']=='rbk': return redirect('/rbk_index')
    
    return render_template('base.html', temp=active_user)


#login route
@app.route('/login', methods=["GET","POST"])
def login():
    if not session.get('logged_in'):
        if request.method=='POST':
            form = request.form
            form_phone = form['username']
            form_password = form['password']

            con = get_db()
            cursor = con.execute('SELECT * FROM users')
            rows = cursor.fetchall()

            for row in rows:
                db_user = dict(row)

                if form_phone == db_user['phone'] and form_password == db_user['password']:
                    session['logged_in'] = True
                    del db_user['password']
                    session['active_user'] = db_user
                    return redirect('/')
            else:
                return render_template('login', alert_script='<script>alert("Invalid login credentials. Retry again.")</script>')
        else:
            return render_template('login', alert_script='')
    else:
        return redirect('/')


#logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login')




#signup route
@app.route('/signup')
def signup():
    return render_template('signup')

#contact us route
@app.route('/contactus')
def contactus():
    return render_template('contactus')

@app.route('/msg', methods=["POST","GET"])
@login_required
def send_msg():
    if request.method=="POST":
        data = request.get_json()
        con = get_db()
        con.execute(f'INSERT INTO messages (c_fullname, c_phone, survey_no, message) VALUES (?,?,?,?)',
                    (data['c_fullname'], data['c_phone'], data['survey_no'], data['message']) )
        con.commit()
        return jsonify({'status':'ok'})




user_reg_mandal = ''
user_reg_village = ''
user_type = ''

@app.route('/rbk_reg', methods=["GET","POST"])
def rbk_reg():
    return render_template('rbk_reg', title='RBK Registration form')

@app.route('/ricemill_reg', methods=["GET","POST"])
def ricemill_reg():
    if request.method=="GET":
        global user_reg_mandal
        global user_reg_village
        global user_type

        user_reg_mandal = request.args.get('mandal')
        user_reg_village = request.args.get('village')
        user_type = 'ricemill'
        
        return render_template('ricemill_reg', reg_type="ricemill_reg")
        
    
    if request.method=="POST":
        data = request.get_json()

        con = get_db()
        con.execute('INSERT INTO users  (phone, password, user_type) VALUES (?,?,?)', 
                    (data['mill_phone'], data['password'], user_type))
        con.execute('INSERT INTO ricemill_owners (fullname, millname, mill_phone, storage_capacity, milling_capacity, dispatched_bags, address, mandal, village) VALUES (?,?,?,?,?,?,?,?,?)', 
                    (data['fullname'], data['millname'], data['mill_phone'], data['storage_capacity'], data['milling_capacity'], 0, data['address'], user_reg_mandal, user_reg_village))
        
        con.commit()

        return jsonify({'status':'ok'})

@app.route('/farmer_reg', methods=["GET","POST"])
def farmer_reg():
    if request.method=="GET":
        global user_reg_mandal
        global user_reg_village
        global user_type

        user_reg_mandal = request.args.get('mandal')
        user_reg_village = request.args.get('village')
        user_type = 'farmer'
        
        return render_template('farmer_reg', reg_type="farmer_reg")
        
    
    if request.method=="POST":
        data = request.get_json()

        con = get_db()
        con.execute('INSERT INTO users  (phone, password, user_type) VALUES (?,?,?)', 
                    (data['phone'], data['password'], user_type))
        con.execute('INSERT INTO farmers  (fullname, phone, bank_ac, aadhaar_no, address, mandal, village) VALUES (?,?,?,?,?,?,?)', 
                    (data['fullname'], data['phone'], data['bank_ac'], data['aadhaar_no'], data['address'], user_reg_mandal, user_reg_village))
        con.execute('INSERT INTO surveys  (phone, survey_no, land_capacity, land_passbook) VALUES (?,?,?,?)', 
                    (data['phone'], data['survey_no'], data['land_capacity'], data['land_passbook'],))
        
        con.commit()

        return jsonify({'status':'ok'})



@app.route('/transport_reg', methods=["GET","POST"])
def transport_reg():
    if request.method=="GET":
        global user_reg_mandal
        global user_reg_village
        global user_type

        user_reg_mandal = request.args.get('mandal')
        user_reg_village = request.args.get('village')
        user_type = 'transport'
        
        return render_template('transport_reg', reg_type="transport_reg")
        
    
    if request.method=="POST":
        data = request.get_json()

        con = get_db()
        con.execute('INSERT INTO users  (phone, password, user_type) VALUES (?,?,?)', 
                    (data['phone'], data['password'], user_type))
        con.execute('INSERT INTO transport_owners (fullname, phone, vehicle_type, vehicle_no, vehicle_rec, available_dates, address, mandal, village) VALUES (?,?,?,?,?,?,?,?,?)', 
                    (data['fullname'], data['phone'], data['vehicle_type'], data['vehicle_no'], data['vehicle_rec'], '[]', data['address'], user_reg_mandal, user_reg_village))
        
        con.commit()

        return jsonify({'status':'ok'})





@app.route('/rbk_index')
def rbk_index():
    return render_template('rbk_index', temp='')

@app.route('/ricemill_index')
def ricemill_index():
    active_user = session.get('active_user')

    if active_user['user_type']=='ricemill':
        con = get_db()

        mill_phone = active_user['phone']
        cursor = con.execute(f'SELECT * FROM ricemill_owners where mill_phone="{ mill_phone }"')
        mill_details = [dict(each) for each in cursor.fetchall()][0]

        millname = mill_details['millname']
        cursor = con.execute(f'SELECT * FROM ricemill_queue where millname="{ millname }"')
        mill_queue = [dict(each) for each in cursor.fetchall()]

        return render_template('ricemill_index', user_details=mill_details, queue=mill_queue)
    else:
        return '<h3>Error : You does not have access to this page.</h3>'



@app.route('/mill_update/<type_>', methods=["POST","GET"])
def mill_update(type_):
    active_user = session.get('active_user')

    if request.method=="POST":
        if type_=='bags_status':
            data = request.get_json()

            con = get_db()

            if data['status']=='dispatched':

                phone = active_user['phone']
                cursor = con.execute(f'SELECT storage_capacity, dispatched_bags FROM ricemill_owners WHERE mill_phone={phone}')
                record = [dict(each) for each in cursor.fetchall()][0]
                 
                storage_capacity = record['storage_capacity'] - int(data['no_of_bags']) 
                dispatched_bags = record['dispatched_bags'] + int(data['no_of_bags'])

                con.execute(f'UPDATE ricemill_owners SET storage_capacity=?, dispatched_bags=?  WHERE mill_phone=?',
                            ( storage_capacity, dispatched_bags , active_user['phone'] ) )

            con.execute(f'UPDATE ricemill_queue SET bags_status=? WHERE id=?', ( data['status'], data['id']) )
            con.commit()

            return jsonify({'status':'ok'})
        
        if type_=='mill':
            form = request.get_json()

            con = get_db()
            con.execute(f'UPDATE ricemill_owners SET storage_capacity=?, milling_capacity=?, dispatched_bags=?  WHERE mill_phone=?',
                         ( form['storage_capacity'], form['milling_capacity'], form['dispatched_bags'], active_user['phone'] ) )
            con.commit()

            return jsonify({'status':'ok'})



@app.route('/farmer_index')
@login_required
def farmer_index():
    active_user = session.get('active_user')

    if active_user['user_type']=='farmer':
        con = get_db()

        phone = active_user['phone']

        cursor = con.execute(f'SELECT * FROM farmers where phone="{ phone }"')
        farmer_details = [dict(each) for each in cursor.fetchall()][0]

        
        cursor = con.execute(f'SELECT * FROM surveys where phone="{ phone }"')
        surveys = [dict(each) for each in cursor.fetchall()]

        crops = []
        for each_survey in surveys:
            survey_no = each_survey['survey_no']
            cursor = con.execute(f'SELECT * FROM crops_queue where survey_no="{ survey_no }"')
            for each in cursor.fetchall():
                crops.append(dict(each))
        
        transports = []
        for each_crop in crops:
            crop_id = each_crop['crop_id']
            cursor = con.execute(f'SELECT * FROM transport_queue where crop_id="{ crop_id }"')
            for each in cursor.fetchall():
                transports.append(dict(each))
        
        return render_template('farmer_index', user_details=farmer_details, surveys=surveys, crops=crops, transports=transports)
    
    else:
        return '<h3>Error : You does not have access to this page.</h3>'

@app.route('/crops_sell', methods=["POST"])
def crops_sell():
    active_user = session.get('active_user')
    data = request.get_json()
    con = get_db()

    columns = ', '.join(data.keys())
    placeholders = ', '.join('?' * len(data))
    sql = 'INSERT INTO crops_queue ({}) VALUES ({})'.format(columns, placeholders)
    values = [v for k,v in data.items()]

    con.execute(sql, values)
    con.commit()

    return jsonify({'status':'ok'})



@app.route('/transport_index')
@login_required
def transport_index():
    active_user = session.get('active_user')

    if active_user['user_type']=='transport':
        con = get_db()

        phone = active_user['phone']

        cursor = con.execute(f'SELECT * FROM transport_owners where phone="{ phone }"')
        transport_owner_details = [dict(each) for each in cursor.fetchall()][0]
        
        cursor = con.execute(f'SELECT * FROM transport_queue where d_phone="{ phone }"')
        transport_queue = [dict(each) for each in cursor.fetchall()]
        
        return render_template('transport_index', user_details=transport_owner_details, queue=transport_queue)
    
    else:
        return '<h3>Error : You does not have access to this page.</h3>'


@app.route('/transport_update/<type_>', methods=["POST"])
def transport_update(type_):
        if type_=='available_dates':
            data = request.get_json()

            con = get_db()
            con.execute(f'UPDATE transport_owners SET available_dates=? WHERE phone=?', ( data['available_dates'], data['phone']) )
            con.commit()

            return jsonify({'status':'ok'})
        if type_=='track_status':
            data = request.get_json()
            print(data)

            con = get_db()
            con.execute(f'UPDATE transport_queue SET status=? WHERE track_id=?', ( data['status'], data['track_id']) )
            con.commit()

            return jsonify({'status':'ok'})


if __name__=="__main__":
    app.run(debug=True)