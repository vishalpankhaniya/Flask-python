from flask import Flask, request, flash, url_for, redirect, render_template,jsonify  
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy 
from werkzeug import secure_filename
from flask_mail import Mail, Message
from datetime import date

app = Flask(__name__)
bcrypt = Bcrypt()

app.secret_key = "TriviaPost"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/social'  

mysql = MySQL()
mysql.init_app(app)
mail = Mail(app)


# MySql Connection Here

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'social'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'raoinfotechp@gmail.com'
app.config['MAIL_PASSWORD'] = 'raoinfotech@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)



# Function For Singup

@app.route('/signup', methods = ['GET', 'POST'])
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
            msg = Message('', sender = 'raoinfotechp@gmail.com', recipients = [email])
            msg.body = "Thanks For Registering With Us"
            mail.send(msg)
            flash('Record was successfully added')   
            return {'message': 'Registered Successfully'}


# Function For Login

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

# Function For  User List
 
@app.route('/userList', methods = ['GET'])
def userList():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM user')
    found_user = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    today = date.today()
    print("Today's date:", today)
    return render_template('userList.html', User = found_user ) 

# Function For Edit Profile 

@app.route('/editprofile', methods = ['POST'])
def editprofile():
    if request.method == 'POST':
        if not request.form['fname'] or not request.form['lname'] or not request.form['email']:
            flash('Please enter all the fields', 'error')
        else:
            details = request.form
            uid = details['uid']
            fname = details['fname']
            lname = details['lname']
            email = details['email']
            cur = mysql.connection.cursor()
            cur.execute('UPDATE `user` SET `fname`=%s,`lname`=%s,`email`=%s WHERE `uid` =%s',[fname,lname,email,uid])
            mysql.connection.commit()
            cur.close()
            flash('Record was updated successfully')   
            return {'message': 'User Updated Successfully'}


#  Functin For Delete User

@app.route('/user', methods = ['DELETE'])
def deleteUser():
    details = request.form
    uid = details['uid']
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM `user` WHERE `uid`=%s',[uid])
    mysql.connection.commit()
    cur.close()
    flash('User Deleted Successfully')   
    return {'message': 'User Deleted Successfully'}

# Function for Add New Post
 
@app.route('/post', methods = ['GET', 'POST'])
def addPost():
    if request.method == 'POST':
        if not request.form['userId'] or not request.form['title'] or not request.form['content']:
            flash('Please enter all the fields', 'error')
        else:
            details = request.form
            userId = details['userId']
            title = details['title']
            content = details['content']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO post(userId,title,content) VALUES (%s, %s,%s)", (userId,title,content))
            mysql.connection.commit()
            cur.close()
            flash('Post successfully added')   
            return {'message': 'Post successfully added'}


# Function for Post List Function 

@app.route('/postList', methods = ['GET'])
def postList():
    cur = mysql.connection.cursor()
    cur.execute('SELECT  * FROM post INNER JOIN user ON post.userId=user.uid;')

    # Code For Key Value Pair

    # row_headers=[x[0] for x in cur.description]
    # users = cur.fetchall();
    # mysql.connection.commit()
    # cur.close()
    # result = []
    # for user in users:
    #     result.append(dict(zip(row_headers,user)))
    #     return jsonify(result)

    found_post = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template('postList.html', Post = found_post ) 
    flash('Post List Fetch successfully')  
    to_dict(found_post) 
    return str (found_post)



@app.route('/post', methods = ['DELETE'])
def deletePost():
    details = request.form
    postId = details['postId']
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM `post` WHERE `pid`=%s',[postId])
    mysql.connection.commit()
    cur.close()
    return {'message': 'Post Deleted Successfully'}


# Function For File Uploads

@app.route('/uploader', methods = ['POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

# Function For Add User Template Rendering

@app.route('/adduser', methods = ['GET'])
def adduser():
    return render_template('signup.html')  

# Function For Login Template Rendering

@app.route('/userlogin', methods = ['GET'])
def userLogin():
    return render_template('login.html')  

if __name__ == '__main__':
    app.run(debug = True)             