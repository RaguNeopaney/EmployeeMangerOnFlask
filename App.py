from datetime import timedelta
from flask import Flask, render_template, request, redirect,url_for, flash,session,make_response
import pymysql
from flask_session import Session
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY']='123'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
app.config['SESSION_FILE_THRESHOLD'] = 10
Session(app)

conn = pymysql.connect(host='database-1.c6adkfk0nwsn.us-east-2.rds.amazonaws.com',port=3306,user='admin',passwd='123456789',db='CrudDb')
cur = conn.cursor()

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'name' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('Login'))
    return wrap

@app.route('/')
def index():
    return render_template("Login.html")
@app.route('/dashboard')
@is_logged_in
def Dashboard():
    try:
        cur.execute("SELECT * FROM PersonInfo")
        data = cur.fetchall()
        if len(data) < 1:
            flash("There is no data on DB!. Insert some data to see on table","info")
        return render_template("Index.html", person = data)
    except:
        flash("Unable to reterieve data","warning")
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
        session.pop('name', None)
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
                session["name"] = request.form['Email']
                return redirect(url_for('Dashboard'))
            else:
                flash('Username or Password is incorrect!!', 'danger')
                return redirect(url_for('Login'))
        else:
            flash("User not found. Register Here!!", "warning")
            return redirect(url_for('Registrations'))
    return render_template("Login.html")
@app.route('/logout')
def Logout():
    session.pop('name', None)
    session.clear()
    flash("logout successfully","info")
    response = make_response(redirect(url_for('Login')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response
@app.route('/addpersons',methods=['GET','POST'])
@is_logged_in
def Addpersons():
    if request.method == 'POST':
        FirstName = request.form['Firstname']
        LastName = request.form['Lastname']
        EmailAddress = request.form['Email']
        try:
            cur.execute("SELECT * FROM PersonInfo WHERE FirstName = %s AND LastName = %s AND Email = %s", (FirstName, LastName, EmailAddress))
            personreqres = cur.fetchall()
            if len(personreqres) >= 1:
                flash("A person already exist in the table. Add other person", 'danger')
                return redirect(url_for('Addpersons'))
            else:
                cur.execute("INSERT INTO PersonInfo (FirstName, LastName, Email) VALUES (%s,%s,%s)",(FirstName, LastName, EmailAddress))
                conn.commit()
                flash("Person information added successfully","success")
                return redirect(url_for('Addpersons'))               
        except:
            flash("Trouble Adding person!", "danger")
            return redirect(url_for('Dashboard'))
    return render_template('AddPerson.html')
@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'POST':
        personId = request.form['personid']
        FirstName = request.form['FirstName']
        LastName = request.form['LastName']
        Email = request.form['Email']
        try:
            cur.execute("UPDATE PersonInfo SET FirstName = %s, LastName = %s,Email = %s WHERE idPersonInfo = %s",(FirstName, LastName, Email, personId))
            conn.commit()
            flash("Information Updated","info")
            return redirect(url_for("Dashboard"))
        except:
            flash("Error Updating Info","info")
            return redirect(url_for("Dashboard"))
    else:
        return redirect(url_for("Dashboard"))
@app.route('/delete',methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        personId = request.form['personid']
        try:
            cur.execute("DELETE FROM PersonInfo WHERE idPersonInfo = %s", (personId))
            conn.commit()
            flash("The person info has been deleted.","warning")
            return redirect(url_for("Dashboard"))
        except:
            flash("Error while processing your delete request")
            return redirect(url_for("Dashboard"))
    else:
        return redirect(url_for("Dashboard"))
if __name__ == "__main__":
    app.run()
