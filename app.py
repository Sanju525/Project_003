from flask import Flask,render_template,session,redirect,flash,url_for,request
import yaml
import pdfkit
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
Bootstrap(app)


# ======================================================================== #

#DB Configurations
# server :: Development
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

app.config['SECRET_KEY'] = os.urandom(24)

# ======================================================================== #

#DB Configurations
# server :: Production


# ======================================================================== #
# Applications Route
# ======================================================================== #
# Login page / ?? / Index page
@app.route('/', methods=['GET', 'POST'])
def login():
    session['login'] = False
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM studentsignlogs WHERE username = %s", ([username]))
        print(resultValue)
        if resultValue > 0:
            user = cur.fetchone()
            if userDetails['password'] == user['password']:
                session['login'] = True
                session['username'] = user['username']
                session['email'] = user['email']
                flash('Welcome..! You have been successfully logged in', 'success')
                # return "Welcome to home page"
                return render_template('home.html')
            else:
                cur.close()
                flash('Password does not match', 'danger')
                return render_template('log_in.html')
        else:
            cur.close()
            flash('User not found', 'danger')
            return render_template('log_in.html')
        cur.close()
        return redirect('/')
    return render_template('log_in.html')
# ======================================================================== #

# ======================================================================== #
# signup page / userloginRegistration page
@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    session['login'] = False
    if request.method == 'POST':
        userDetails = request.form
        # try:
        print(userDetails)
        if userDetails['password'] != userDetails['confirm_password']:
            flash('Passwords do not match! Try again.', 'danger')
            return render_template('signup.html')
        # except MySQLdb._exceptions.IntegrityError:
        #     flash('Credentials already exits! try again', 'danger')
        #     return render_template('signup.html')
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO studentsignlogs(username, email, phone ,password) VALUES(%s,%s,%s,%s)",(userDetails['username'], userDetails['email'],userDetails['phone'], userDetails['password']))
            mysql.connection.commit()
            cur.close()
            flash('Registration successful! Please Fill the registration form.', 'success')
            return redirect('/student-register')
        except mysql.connection.IntegrityError as err:
            flash('Credentials already exits! try again', 'danger')
            return render_template('sign-up.html')

    return render_template('sign-up.html')

# ======================================================================== #

# ======================================================================== #
# Booking page
@app.route('/Booking/Student-Register', methods=['GET', 'POST'])
def student_register():
    try:
        if session['login'] == True:
            if request.method == 'POST':
                Student_details = request.form
                # print(Student_details)
            return render_template('BookingForm.html')
    except:
        return render_template('404NF.html')

# ======================================================================== #

# ======================================================================== #
# Home page
@app.route('/home')
def home():
    try:
        if session['login'] == True:
            return render_template('home.html')
    except:
        flash("Please login ",'danger')
        return render_template('404NF.html')

# ======================================================================== #
# Features
@app.route('/features')
def feat():
    return render_template('features.html')

# ======================================================================== #

# ======================================================================== #
# Rom check
@app.route('/roomcheck')
def rooms():
    return render_template('RoomCheck.html')


# ======================================================================== #
# Session logout
@app.route('/logout/')
def logout():
    session.clear()
    flash("You have been logged out", 'info')
    return redirect('/')

# ======================================================================== #

# ======================================================================== #
# Running the application
if __name__ == '__main__':
    app.run(debug=True)

# ======================================================================== #
