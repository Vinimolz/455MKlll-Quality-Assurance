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
                #ipassword = auth_functions.hash_User_Password(ipassword)
                ipassword = sha256_crypt.encrypt(ipassword)
                print(ipassword)
                cursor.execute('INSERT INTO Customer VALUES (NULL, % s, % s, % s, % s)', ( 
                    ifirstname, 
                    ilastname,
                    iemail, 
                    ipassword))

                mysql.connection.commit()
                flash('user created sucessfully')
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
                print("Before auth login function")
                print(db_password[0])
                #if auth_functions.verify_User_Password(password, db_password[0]):
                if sha256_crypt.verify(password, db_password[0]):

                    session['loggedin'] = True
                    session['id'] = account_info[0]
                    session['firstName'] = account_info[1]
                    
                    flash('You are logged in!', category='sucess')
                    print('Loggin sucessful')
                    return redirect(url_for('ecommerce'))

                else:
                    flash('Incorrect password', category='error')
                    print('Incorrect password')
            else:
                flash('username does not exist', category='error')
                print('Username does not exists')

        return render_template("login.html")
    
    #---------------------------------------> Logout Function <-------------------------------------------
    # Function for a future logout button that can only be accessed if user is logged in 
    @app.route("/logout")
    #@login_required
    def logout():
        if session["loggedin"] == True:
            session.pop('firstName')
            session.pop('id')
            session["loggedin"] = False
            flash("You have been logged out", category='sucess')
            return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

    #-------------------------------- This will be our future ecommerce main page --------------------------    @app.route('/ecommerce', methods=['GET', 'POST'])
    @app.route("/ecommerce", methods=['GET', 'POST'])
    def ecommerce():
        try:            
            if session['loggedin']:
                shoeList = fetchAllShoes()
                return render_template("ecommerce.html", username = session['firstName'], id = session['id'], sendList = shoeList)
            else:
                session['loggedin'] = False
                session['firstName'] = "Store Guest"
                session['id'] = -1
                shoeList = fetchAllShoes()
                print("passed by else statement (user loggedin == false)")
                return render_template("ecommerce.html", username = session['firstName'], id = session['id'], sendList = shoeList)

        except:
            flash("Something went wrong :'(", category='error')
            return redirect(url_for('login'))

        finally:
            if request.method == 'POST':
                formBrand = request.form.get("brand")
                formType = request.form.get("type")
                formColor = request.form.get("color")
                formSex = request.form.get("sex")

                print(formBrand)
                print(formType)
                print(formColor)
                print(formSex)

                searchShoeList = userShoeSearch(brand=formBrand, type=formType, color=formColor, sex=formSex)
                print("After function call") 
                return render_template("ecommerce.html", username = session['firstName'], id = session['id'], sendList = searchShoeList)

#------------------------------- Single Model view Page -----------------------------------------------------
    @app.route('/ecommerce/modelview/<int:shoeid>')
    def testingroute(shoeid):
        #Query to fetch shoe info from inventory by ShoeID and InventoryID
        InventoryInfo = fetchInfoFromInventory(shoeid)
        ShoeInfo = fetchShoeInfo(shoeid)
        for i in InventoryInfo:
            print(i)
        
        print(ShoeInfo)
        #Query to add shoe to cart if user is loggedin
        return render_template("modelview.html", sendID = shoeid)

#-------------------------------- This will be our future cart page --------------------------------------
    @app.route('/ecommerce/cart')
    def cart():
        try:
            try:
                return render_template("cart.html", 
                    username = session['firstName'], 
                    user_id = session['id'])
            except:
                session["loggedin"] = False
                return render_template("cart.html", 
                    username = "Store Guest",
                    user_id = -1)
        except:
            flash("Something went wrong :'(", category='error')
            return redirect(url_for('ecommerce'))

    #-------------------------------- This will be our future profile page ----------------------------
    @app.route('/ecommerce/profile')
    @login_required
    def profile():
        return render_template("profile.html", 
            username = session['firstName'], 
            user_id = session['id'])

    #------ This will be our recover password page that will most likely not be fully implemented--------
    @app.route('/recoverpasswd', methods=['GET', 'POST'])
    def recoverpasswd():
        return render_template("recoverpasswd.html")

    #---------- This will be our contact page that will most likely not be fully implemented--------------
    @app.route('/ContactUs')
    def contact():
        return render_template("aboutUs.html")

    def fetchInfoFromInventory(shoeId):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('SET @element = % s' , (shoeId, ))
            cursor.execute('SELECT * FROM Inventory WHERE ShoeID = @element')
            InventoryInfo = cursor.fetchall()
        except:
            print("Problem with fetchInfoFromInventory function")
        return InventoryInfo

    def fetchShoeInfo(shoeId):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('SET @element = % s' , (shoeId, ))
            cursor.execute('SELECT * FROM Shoes WHERE ShoeID = @element')
            shoe = cursor.fetchone()
        except:
            print("Problem with fetchShoeInfo function")
        return shoe

    def fetchAllShoes():
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT DISTINCT Shoes.ShoeID, ShoeName, CustPrice, Brand, ShoeType, Color, Gender, PicturePath FROM Shoes, Inventory WHERE Shoes.ShoeID = Inventory.ShoeID AND Quantity > 0;')
        allShoes = cursor.fetchall()
        for shoe in allShoes:
            print(shoe)
        return allShoes

    def userShoeSearch(brand, type, color, sex):
        cursor = mysql.connection.cursor()
        if brand != None and type != None and color != None and sex != None: 
            cursor.execute('SELECT DISTINCT Shoes.ShoeID, ShoeName, CustPrice, Brand, ShoeType, Color, Gender, PicturePath FROM Shoes, Inventory WHERE Shoes.ShoeID = Inventory.ShoeID AND Brand = % s AND ShoeType = % s AND Color = % s AND Gender = % s' , (brand, type, color, sex,  ))
            shoeSearch = cursor.fetchall()

        elif brand != None and type == None and color == None and sex == None:
            cursor.execute('SELECT DISTINCT Shoes.ShoeID, ShoeName, CustPrice, Brand, ShoeType, Color, Gender, PicturePath FROM Shoes, Inventory WHERE Shoes.ShoeID = Inventory.ShoeID AND Brand = % s' , (brand, ))
            shoeSearch = cursor.fetchall()

        elif brand == None and type != None and color == None and sex == None:
            cursor.execute('SELECT DISTINCT Shoes.ShoeID, ShoeName, CustPrice, Brand, ShoeType, Color, Gender, PicturePath FROM Shoes, Inventory WHERE Shoes.ShoeID = Inventory.ShoeID AND ShoeType = % s' , (type, ))
            shoeSearch = cursor.fetchall()

        elif brand == None and type == None and color != None and sex == None:
            cursor.execute('SELECT DISTINCT Shoes.ShoeID, ShoeName, CustPrice, Brand, ShoeType, Color, Gender, PicturePath FROM Shoes, Inventory WHERE Shoes.ShoeID = Inventory.ShoeID AND Color = % s' , (color, ))
            shoeSearch = cursor.fetchall()

        elif brand == None and type == None and color == None and sex != None:
            cursor.execute('SELECT DISTINCT Shoes.ShoeID, ShoeName, CustPrice, Brand, ShoeType, Color, Gender, PicturePath FROM Shoes, Inventory WHERE Shoes.ShoeID = Inventory.ShoeID AND Gender = % s' , (sex, ))
            shoeSearch = cursor.fetchall()

        else:
            print("Did not work")
        for shoe in shoeSearch:
            print(shoe)
        return shoeSearch

    return app