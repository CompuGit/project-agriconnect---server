import sqlite3
con = sqlite3.connect('./database.db')
con.row_factory = sqlite3.Row

user_data_insert = '''INSERT INTO users 
    (username, password, user_type)
    values('admin','123456','admin')'''

#con.execute(user_data_insert)
#con.commit()

db_users = 'SELECT * FROM users'
#cursor = con.execute()
#users = cursor.fetchall()
#con.close()
#print(users)