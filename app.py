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





@app.route('/rbk_reg', methods=["GET","POST"])
def rbk_reg():
    return render_template('rbk_reg', title='RBK Registration form')

@app.route('/ricemill_reg', methods=["GET","POST"])
def ricemill_reg():
    return render_template('ricemill_reg', title='Ricemiller Registration form')

@app.route('/farmer_reg', methods=["GET","POST"])
def farmer_reg():
    return render_template('farmer_reg', title='Farmer Registration form')

@app.route('/transport_reg', methods=["GET","POST"])
def transport_reg():
    return render_template('transport_reg', title='Transport Registration form')




@app.route('/msg', methods=["POST","GET"])
@login_required
def send_msg():
    if request.method=="POST":
        data = request.get_json()

        con = get_db()
        con.execute(f'INSERT INTO messages (c_fullname, c_phone, survey_no, message) VALUES (?,?,?,?)', (data['c_fullname'], data['c_phone'], data['survey_no'], data['message']) )
        con.commit()

        return jsonify({'status':'ok'})




@app.route('/rbk_index')
def rbk_index():
    return render_template('rbk_index', temp='')

@app.route('/ricemill_index')
def ricemill_index():
    return render_template('ricemill_index', temp='')

@app.route('/farmer_index')
def farmer_index():
    con = get_db()

    active_user = session.get('active_user')
    phone = active_user['phone']

    cursor = con.execute(f'SELECT * FROM farmers where phone="{ phone }"')
    farmer_details = [dict(each) for each in cursor.fetchall()]

    
    cursor = con.execute(f'SELECT * FROM surveys where phone="{ phone }"')
    surveys = [dict(each) for each in cursor.fetchall()]
    crops = []
    for each_survey in surveys:
        survey_no = each_survey['survey_no']
        cursor = con.execute(f'SELECT * FROM crops_queue where survey_no="{ survey_no }"')
        for each in cursor.fetchall():
            crops.append(dict(each))
    
    return render_template('farmer_index', user_details=farmer_details[0], surveys=surveys, crops=crops)

@app.route('/transport_index')
def transport_index():
    con = get_db()

    active_user = session.get('active_user')
    phone = active_user['phone']

    cursor = con.execute(f'SELECT * FROM transport_owners where phone="{ phone }"')
    transport_owner_details = [dict(each) for each in cursor.fetchall()]
    
    cursor = con.execute(f'SELECT * FROM transport_queue where d_phone="{ phone }"')
    queue = [dict(each) for each in cursor.fetchall()]
     
    return render_template('transport_index', user_details=transport_owner_details[0], queue=queue)


@app.route('/transport_update/<type_>', methods=["POST","GET"])
def transport_update(type_):
    if request.method=="POST":
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