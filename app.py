import sqlite3
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
    if active_user['user_type']=='farmer': return render_template('farmer_index', temp=active_user)
    if active_user['user_type']=='transport': return render_template('transport_index', temp=active_user)
    if active_user['user_type']=='ricemill': return render_template('ricemill_index', temp=active_user)
    if active_user['user_type']=='rbk': return render_template('rbk_index', temp=active_user)
    
    return render_template('base.html', temp=active_user)


#login route
@app.route('/login', methods=["GET","POST"])
def login():
    if not session.get('logged_in'):
        if request.method=='POST':
            form = request.form
            form_username = form['username']
            form_password = form['password']

            con = get_db()
            cursor = con.execute('SELECT * FROM users')
            rows = cursor.fetchall()

            for row in rows:
                db_user = dict(row)

                if form_username == db_user['username'] and form_password == db_user['password']:
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
    return render_template('rbkreg', title='RBK Registration form')

@app.route('/ricemill_reg', methods=["GET","POST"])
def ricemill_reg():
    return render_template('ricemill_reg', title='Ricemiller Registration form')

@app.route('/farmer_reg', methods=["GET","POST"])
def farmer_reg():
    return render_template('farmer_reg', title='Farmer Registration form')

@app.route('/transport_reg', methods=["GET","POST"])
def transport_reg():
    return render_template('transport_reg', title='Transport Registration form')






@app.route('/rbk_index')
def rbk_index():
    return render_template('rbk_index', temp='')

@app.route('/ricemill_index')
def ricemill_index():
    return render_template('ricemill_index', temp='')

@app.route('/farmer_index')
def farmer_index():
    return render_template('farmer_index', temp='')

@app.route('/transport_index')
def transport_index():
    return render_template('transport_index', temp='')


if __name__=="__main__":
    app.run(debug=True)