from flask import Blueprint, render_template, session
from flask_mysqldb import MySQL

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/landpage")
def landpage():
        return render_template("landpage.html")

@views.route("/testimonials")
def testimonials():
        return render_template("testimonials.html")

@views.route("/aboutUs")
def aboutUs():
        return render_template("aboutUs.html")

