from flask import Blueprint, render_template, session
from flask_mysqldb import MySQL

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/landpage")
def landpage():
        if "loggedin" not in session:
                session["loggedin"] = False
                print("assigned loggedin False")
                return render_template("landpage.html")
        else:   
                print("Did not re assigned loggedin")
                print(session['loggedin'])
                return render_template("landpage.html")

@views.route("/testimonials")
def testimonials():
        return render_template("testimonials.html")

@views.route("/aboutUs")
def aboutUs():
        return render_template("aboutUs.html")

