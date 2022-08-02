from flask import Flask, render_template,request,json,url_for,session,flash,redirect
from flask_mysqldb import MySQL
import os
from werkzeug.security import generate_password_hash as gen, check_password_hash as check
import math

app = Flask(__name__)


with open('vars.json','r') as v:
    variable = json.load(v)

db_keeps = variable["sql_conf"]



mysql = MySQL(app)
# MySQL Configuration
app.config['MYSQL_HOST'] = db_keeps["mysql_host"]
app.config['MYSQL_USER'] = db_keeps["mysql_user"]
app.config['MYSQL_PASSWORD'] = db_keeps["mysql_password"]
app.config['MYSQL_DB'] = db_keeps["mysql_db"]
app.config['MYSQL_PORT'] = db_keeps['mysql_port']
app.secret_key = os.urandom(24)



@app.route("/")
def home():
    cur = mysql.connection.cursor()
    q = cur.execute("SELECT * FROM blogs where img_link_1 != 'NULL' ORDER BY RAND ( );")
    if q > 0:
        posts = cur.fetchall()
        return render_template('index.html', posts=posts)
    else:
        return render_template('index.html', posts=None)
    

@app.route("/login",methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form
        email = form['email']
        password = form['pass']
        cur = mysql.connection.cursor()
        usercheck = cur.execute("SELECT * FROM user WHERE email_id=%s;", ([email]))
        if usercheck > 0:
            user = cur.fetchone()
            checker = check(user[-2], password)
            if checker:
                session['logged_in'] = True
                session['user'] = user[2]
                session['full_name'] = user[1]
                session['id'] = user[0]
                flash(f"Welcome {session['full_name']}!! Your Login is Successful", 'success')
            else:
                cur.close()
                flash('Wrong Password!! Please Check Again.', 'danger')
                return render_template('login.html', role='customer')
        else:
            cur.close()
            flash('User Does Not Exist!! Please Enter Valid Username.', 'danger')
            return render_template('login.html')
        cur.close()
        return redirect('/')
    return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = request.form
        name = form['name']
        email = form['email']
        number = form['contact']
        password = gen(form['pass'])
        cur = mysql.connection.cursor()
        usercheck = cur.execute("SELECT * FROM user;")
        if usercheck>0:
            users = cur.fetchall()
            for user in users:
                if (user[2] == email) or (user[3] == number):
                    flash("User Already Exists!, Please Login...")
                    return redirect('login')
        cur.execute("INSERT INTO user (full_name,email_id,password,contact) values (%s,%s,%s,%s);", (name,email,password,number))
        mysql.connection.commit()
        cur.close()
        return redirect('/login')

    return render_template("register.html")

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if 'user' in session:
        if request.method == 'POST':
            form = request.form
            user_id = session['id']
            msg = form['msg']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO contact (person_id,msg) VALUES (%s,%s);", (user_id,msg))
            mysql.connection.commit()
            cur.close()
            return redirect('/')
        return render_template('contact.html')
    return redirect('/')

@app.route("/logout")
def logout():
    if 'user' in session:
        session['logged_in'] = False
        session.pop('user') 
        session.pop('full_name') 
        session.pop('id')
        flash('User Logged Out','success')
    return redirect('/')
    
if __name__ == "__main__":
    app.run(debug=True)