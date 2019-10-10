from flask import Flask, request, flash, url_for, redirect, render_template  
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
bcrypt = Bcrypt()


app.secret_key = "TriviaPost"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/social'  

mysql = MySQL()
mysql.init_app(app)

# MySql Connection Here

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'social'



@app.route('/user', methods = ['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        if not request.form['fname'] or not request.form['lname'] or not request.form['email'] or not request.form['password']:
            flash('Please enter all the fields', 'error')
        else:
            details = request.form
            fname = details['fname']
            lname = details['lname']
            email = details['email']
            password = details['password']
            hashpassword = bcrypt.generate_password_hash(password)
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO user(fname, lname, email, password) VALUES (%s, %s,%s,%s)", (fname,lname,email,hashpassword))
            mysql.connection.commit()
            cur.close()
            flash('Record was successfully added')   
            return {'message': 'Registered Successfully'}


@app.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        if not request.form['email'] or not request.form['password']:
            flash('Please enter all the fields', 'error')
        else:
            details = request.form
            email = details['email']
            password = details['password']
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM user WHERE email = %s', [email])
            found_user = cur.fetchone() 
            mysql.connection.commit()       
            cur.close()

        if found_user:
            authenticated_user = bcrypt.check_password_hash(found_user[4],password)
            if authenticated_user:
                return 'Logged in successfully!'
            else:
                return 'Incorrect password!'
        else:
            return 'Incorrect Email!'


@app.route('/userList', methods = ['GET'])
def userList():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM user')
    found_user = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template('userList.html', User = found_user ) 


@app.route('/adduser', methods = ['GET'])
def adduser():
    return render_template('signup.html')  


@app.route('/userlogin', methods = ['GET'])
def userLogin():
    return render_template('login.html')  



if __name__ == '__main__':
    app.run(debug = True)             
