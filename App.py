
from flask import Flask, render_template, request, redirect,url_for, flash
import pymysql

app = Flask(__name__)
conn = pymysql.connect(host='database-1.c6adkfk0nwsn.us-east-2.rds.amazonaws.com',port=3306,user='admin',passwd='123456789',db='CrudDb')
cur = conn.cursor()


@app.route('/')
def index():
    return render_template("Index.html")

@app.route('/Registrationpage')
def Registrations():
    return render_template("Registration.html")

@app.route('/login')
def Login():
    return render_template("Login.html")
    
if __name__ == "__main__":
    app.run()