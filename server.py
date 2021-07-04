import mysql.connector
from flask import Flask, redirect, url_for, request, render_template, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mysql",
    database="his"
)
mycursor = mydb.cursor()

app = Flask(__name__)

app.secret_key = 'secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'his'

# Intialize MySQL
#mysql = MYSQL(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/faq')
def faq():
    return render_template('faq1.html')


@app.route('/ourdoctors')
def ourdoctors():
    mycursor.execute(
        "SELECT CONCAT(`Fname`, ' ', `Lname`) as Name, Qualification FROM doctors")
    # this will extract row headers
    row_headers = [x[0] for x in mycursor.description]
    myresult = mycursor.fetchall()
    return render_template('ViewDoctor.html', headers=row_headers, headersNum=len(row_headers), data=myresult, title='Our', adminPage = False)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        mail = request.form['email']
        messagetype = request.form['type']
        messagedetails = request.form['message']
        sql = "INSERT INTO contact_us (Email, Content,Type) VALUES (%s, %s,%s)"
        val = (mail, messagedetails, messagetype)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template("MessagePage.html")
    else:
        return render_template("ContactUsPage.html")


@app.route('/ViewDoctor')
def viewdoctor():
    mycursor.execute("SELECT * FROM doctors")
    # this will extract row headers
    row_headers = [x[0] for x in mycursor.description]
    myresult = mycursor.fetchall()
    return render_template('ViewDoctor.html', headers=row_headers, headersNum=len(row_headers), data=myresult, title='View', adminPage = True)


@app.route('/ViewPatient')
def viewpatient():
    mycursor.execute("SELECT * FROM patient")
    # this will extract row headers
    row_headers = [x[0] for x in mycursor.description]
    myresult = mycursor.fetchall()
    return render_template('ViewPatient.html', headers=row_headers, headersNum=len(row_headers), data=myresult)


@app.route('/ViewContact')
def viewcontact():
    mycursor.execute("SELECT * FROM contact_us")
    # this will extract row headers
    row_headers = [x[0] for x in mycursor.description]
    myresult = mycursor.fetchall()
    return render_template('ViewContact.html', headers=row_headers, headersNum=len(row_headers), data=myresult)


@app.route('/Admin')
def admin():
    return render_template('Admin.html')


@app.route('/addDoctor', methods=['GET', 'POST'])
def addDoctor():
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        ssn = request.form['ssn']
        id = request.form['id']
        email = request.form['email']
        city = request.form['city']
        address = request.form['address']
        phone = request.form['phone']
        salary = request.form['salary']
        gender = request.form['gender']
        dob = request.form['dob']
        qual = request.form['qual']
        sql = "INSERT INTO doctors (Fname,Lname,SSN,ID,Email,City,Address,Phone,Salary,Gender,DOB,Qualification) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (fname, lname, ssn, id, email, city,
               address, phone, salary, gender, dob, qual)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template("Admin.html")
    else:
        return render_template("AddDoctor.html")


@app.route('/addPatient', methods=['GET', 'POST'])
def addPatient():
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        ssn = request.form['ssn']
        id = request.form['id']
        email = request.form['email']
        city = request.form['city']
        address = request.form['address']
        phone = request.form['phone']
        relativephone = request.form['relphone']
        dob = request.form['dob']
        docid = request.form['docid']
        maritalstat = request.form['maritalstat']
        occ = request.form['occ']
        insuranceamt = request.form['insuranceamt']

        sql = "INSERT INTO patient (Fname,Lname,SSN,ID,Email,DOB,Phone,MaritalStatus,RelativePhone,InsuranceAmount,City,Address,Occupation,D_ID) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (fname, lname, ssn, id, email, dob, phone, maritalstat,
               relativephone, insuranceamt, city, address, occ, docid)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template("Admin.html")
    else:
        return render_template("AddPatient.html")


@app.route('/SignIn')
def signin():
    return render_template('AdminLogin.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'adminid' in request.form and 'password' in request.form:
        adminid = request.form['adminid']
        password = request.form['password']
        cursor = mydb.cursor(dictionary=True)
        cursor.execute('SELECT * FROM support WHERE ID = %s AND S_password = %s', (adminid, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['ID'] = account['SSN']
            session['username'] = account['Fname'] + " " + account['Lname']
            return render_template("Admin.html")
        else:
            error = flash("Invalid Credentials. Please try again.")
            return render_template("AdminLogin.html")


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out

    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
