
from flask import Flask, render_template, request, redirect,url_for, flash
import pymysql


app = Flask(__name__)
app.config['SECRET_KEY']='123'


conn = pymysql.connect(host='database-1.c6adkfk0nwsn.us-east-2.rds.amazonaws.com',port=3306,user='admin',passwd='123456789',db='CrudDb')
cur = conn.cursor()


@app.route('/')
def index():
    return render_template("Index.html")

@app.route('/Registrationpage', methods = ['GET','POST'])
def Registrations():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['Phone']
        password = request.form['password']
        try:
            cur.execute("SELECT * FROM User WHERE Email = %s ", (email))
            dbresult = cur.fetchall()
            if len(dbresult) >= 1:
                flash("Email address already exist. Create new account with different email", "danger")
                return redirect(url_for('Registrations'))
            else:
                cur.execute("INSERT INTO User (Name, Phone, Email,Password) VALUES (%s,%s,%s,%s)",(name, phone, email,password))
                conn.commit()
                flash("Registration complete","success")
                return redirect(url_for('Login'))
        except:
            flash("Trouble Registering! Not Registered", "danger")
            return redirect(url_for('Registrations'))
    return render_template("Registration.html")

@app.route('/login', methods = ['GET','POST'])
def Login():
    if request.method == 'POST':
        useremail = request.form['Email']
        Upassword = request.form['Password']

        cur.execute("SELECT Email, Password FROM CrudDb.User WHERE Email = %s", (useremail))
        result = cur.fetchall()
        if len(result) > 0:
            for r in result:
                for t in r:
                    dbpassword = t
            
            if dbpassword == Upassword:
                flash("Logged in successfully","success")
                return redirect(url_for('index'))
            else:
                flash('Username or Password is incorrect!!', 'danger')
                return redirect(url_for('Login'))
        else:
            flash("User not found. Register Here!!", "warning")
            return redirect(url_for('Registrations'))
    return render_template("Login.html")


if __name__ == "__main__":
    app.run()