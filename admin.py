import sqlite3
from functools import wraps
from flask import Flask, g, request, session, redirect, url_for, jsonify, render_template

app = Flask(__name__)
app.secret_key = 'my_admin_secret_key'
app.config['SESSION_COOKIE_NAME'] = 'rbk_app_session'
app.config['DATABASE'] = './database.db'

app.jinja_env.globals.update(format=format)

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
        if session.get('rbk_logged_in'):
            return func(*args, **kwargs)
        else:
            return redirect('/login')
    return wraper



#login route
@app.route('/login', methods=["GET","POST"])
def login():
    if not session.get('rbK_logged_in'):
        if request.method=='POST':
            form = request.form
            form_phone = form['username']
            form_password = form['password']

            con = get_db()
            cursor = con.execute(f'SELECT * FROM rbk_users WHERE phone={form_phone}')
            db_user = dict(cursor.fetchone())


            if form_phone == db_user['phone'] and form_password == db_user['password']:
                    session['rbk_logged_in'] = True
                    del db_user['password']
                    session['rbk_active_user'] = db_user
                    return redirect('/')
            else:
                return render_template('login', title='RBK', alert_script='<script>alert("Invalid login credentials. Retry again.")</script>', page='/rbk_reg')
        else:
            return render_template('login', title='RBK', alert_script='', page='/rbk_reg')
    else:
        return redirect('/')


#logout route
@app.route('/logout')
def logout():
    session.pop('rbk_logged_in', None)
    session.pop('rbk_active_user', None)
    return redirect('/login')




#signup route
@app.route('/signup')
def signup():
    return render_template('signup')

#contact us route
@app.route('/contactus')
def contactus():
    return render_template('contactus')

@app.route('/messages', methods=["GET"])
#@login_required
def messages():
    con = get_db()
    cursor = con.execute(f'SELECT * FROM messages' )
    rows = [dict(each) for each in cursor.fetchall()]

    return jsonify(rows)




@app.route('/rbk_reg', methods=["POST","GET"])
def rbk_reg():
    if request.method=='GET':
        return render_template('rbk_reg', title='RBK Registration form', reg_type='rbk_reg')
    if request.method=='POST':
        data = request.get_json()
        con = get_db()
        con.execute(f'INSERT INTO rbk_users (fullname, password, phone, mandal, village) VALUES (?,?,?,?,?)',
                (data['fullname'], data['password'], data['phone'], data['mandal'], data['village']) )
        con.commit()
        return jsonify({'status':'ok'})

#default route
@app.route('/')
@login_required
def index():
    rbk_active_user = session.get('rbk_active_user')
    con = get_db()
    
    mandal = rbk_active_user['mandal']
    cursor = con.execute(f'SELECT * FROM crops_queue WHERE  status="Processing"')
    crops_queue = [dict(each) for each in cursor.fetchall()]
    print(crops_queue)

    return render_template('rbk_index', user_details=rbk_active_user, crops_queue=crops_queue)

if __name__=="__main__":
    app.run(debug=True, port=5001)