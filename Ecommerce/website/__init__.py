from flask import Flask, render_template,redirect, url_for, request, flash, session
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from functools import wraps
from os import path
import re
from website import auth_functions

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'CSSE490'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'QAproject'
 
    from .views import views
    app.register_blueprint(views, url_prefix = "/")

    mysql = MySQL(app)

    # -------------------------------------> Login Requeriment function <--------------------------------------
    # If we ever need a function that only allow users to access a certain page if they are logged in 
    def login_required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if 'loggedin' in session:
                return f(*args, **kwargs)
            else:
                flash("You need to login first")
                return redirect(url_for('login'))
        return wrap

    #----------------------------------------> Signup function <----------------------------------------------

    @app.route("/signup", methods=['GET', 'POST'])
    def signup():    

        if request.method == "POST":    
            ifirstname = request.form.get("firstName")
            ilastname = request.form.get("lastName")
            iemail = request.form.get("email")
            ipassword = request.form.get("password")
            iconfirmpassword = request.form.get("confirmPassword")

            cursor = mysql.connection.cursor()

            cursor.execute('SELECT * FROM Customer WHERE email = % s', (iemail, ))
            email_exists = cursor.fetchone()

            if email_exists:
                flash('Email already in use', category='error')
                print("email exists")
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', iemail):
                flash('Not a valid email', category='error')
                print("invalid email")
            elif ipassword != iconfirmpassword:
                flash('Make sure passwords match', category='error')
                print("passwords dont match")
            else:                
                ipassword = auth_functions.hash_User_Password(ipassword)
                print('----------------------PASSWORD STORED-------------------------------------')
                print(ipassword)
                cursor.execute('INSERT INTO Customer VALUES (NULL, % s, % s, % s, % s)', ( 
                    ifirstname, 
                    ilastname,
                    iemail, 
                    ipassword))

                mysql.connection.commit()
                flash('user created sucessfully')
                print('User created')
                return redirect(url_for('login'))

        return render_template("signup.html")

    #----------------------------------------> Login function <----------------------------------------------

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get("email")
            password = request.form.get("password")

            cursor = mysql.connection.cursor()

            cursor.execute('SELECT * FROM Customer WHERE email = % s', (email, ))
            account_info = cursor.fetchone() 

            print(account_info)           

            if account_info:
                
                cursor.execute('SELECT UserPW FROM Customer WHERE email = % s', (email, ) )
                db_password = cursor.fetchone()                

                print(password)
                print(db_password[0])                

                if auth_functions.verify_User_Password(password, db_password[0]):
                    print('db_password == password')

                    session['loggedin'] = True
                    session['id'] = account_info[0]
                    session['firstName'] = account_info[1]
                    
                    flash('You are logged in!')
                    print('Loggin sucessful')
                    return redirect(url_for('ecommerce'))

                else:
                    flash('Incorrect password', category='error')
                    print('Incorrect password')
            else:
                flash('username does not exist', category='error')
                print('Username does not exists')

        return render_template("login.html")
    
    #---------------------------------------> Logout Function <------------------------------------------------
    # Function for a future logout button that can only be accessed if user is logged in 
    @app.route("/logout")
    #@login_required
    def logout():
        if session["loggedin"] == True:
            session.clear()
            flash("You have been logged out", category='success')
            return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

    #-------------------------------- This will be our future ecommerce main page ----------------------------
    @app.route('/ecommerce')
    def ecommerce():
        try:
            try:
                return render_template("ecommerce.html", 
                    username = session['firstName'], 
                    user_id = session['id'])
            except:
                session["loggedin"] = False
                return render_template("ecommerce.html", 
                    username = "Store Guest",
                    user_id = -1)
        except:
            flash("Something went wrong :'(", category='error')
            return redirect(url_for('login'))

    # We can use this for later reference 
    @app.route('/decks', methods=['GET', 'POST'])
    @login_required
    def decks():
        try:
            user_id = session['id']
            username = session['username']
            #query
            return render_template("decks.html", username = session['username'], user_id = session['id'])
        except:
            flash("Something went wrong!", category='error')
            return redirect(url_for('dashboard'))

    # This will be our recover password page that probably will most likely not be fully implemented
    @app.route('/recoverpasswd', methods=['GET', 'POST'])
    def recoverpasswd():
        return render_template("recoverpasswd.html")

    @app.route('/ContactUs')
    def contact():
        return render_template("aboutUs.html")    
    return app