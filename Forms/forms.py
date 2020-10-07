from flask import Blueprint, render_template, session, request, redirect, url_for, flash, jsonify
from admin import admin
from creating_users import allUsers, adminOfApplication
import sqlite3
import datetime
from flask_bcrypt import Bcrypt



forms_bp = Blueprint('forms_bp', __name__, template_folder = 'templates', static_folder = 'static')

bcrypt = Bcrypt()

def check_user_exist(user_email, user_password):
    sqlite_connection = sqlite3.connect('MAIL_DB.db')
    select_query = """SELECT user_email, user_password, user_name FROM user WHERE user_email = ?;"""
    user_record = sqlite_connection.execute(select_query, (user_email,)).fetchall()
    if len(user_record) == 0:
        return False
    for data in user_record:
        if bcrypt.check_password_hash(data[1], user_password):
            return True
    return False

def get_user_name(user_email):
    sqlite_connection = sqlite3.connect("MAIL_DB.db")
    select_query = """SELECT user_name FROM user WHERE user_email = ?;"""
    user_data = sqlite_connection.execute(select_query, (user_email,))
    user_name = ""
    for data in user_data:
        user_name =  data[0]
        break
    sqlite_connection.close()
    return user_name


@forms_bp.route('/')
@forms_bp.route('/LoginForm') #LoginForm
def login_form_page():
    return render_template('Forms/LoginForm.html')

@forms_bp.route('/RegisterationForm') #Registration Form
def registerForm():
    return render_template('Forms/RegisterForm.html')


@forms_bp.route('/ValidLogin', methods = ["POST"]) #Check Validation
def valid_login():
    if request.method == 'POST':

        sqlite_connection = sqlite3.connect('MAIL_DB.db')

        email = request.form['email']
        password = request.form['password']

        check_unauthrized_query = """SELECT user_email FROM unauthorize WHERE user_email = ?;"""
        db_unauthorized_users = sqlite_connection.execute(check_unauthrized_query, (email,))
        for mail in db_unauthorized_users:
            if mail[0] == email:
                flash("unauthorized", "unauthorized")
                return redirect(url_for('forms_bp.login_form_page'))

        select_admin_query = """SELECT * FROM admin WHERE admin_email = 'omar@gmail.com';"""
        db_admin_mail = sqlite_connection.execute(select_admin_query)
        admin_mail = ""
        admin_password = ""
        for admin_data in db_admin_mail:
            admin_mail = admin_data[1]
            admin_password = admin_data[2]
            break
        if admin_password == password and admin_mail == email:
            session['email'] = email
            session['password'] = password
            return redirect(url_for("admin_bp.admin_page"))
        
        if check_user_exist(email, password) == False:
            flash("This Account doesnot Exist", "danger")
            return redirect(url_for("forms_bp.login_form_page"))

        select_query = """SELECT user_password, user_email, user_name FROM user WHERE user_email = ?;"""
        user_record = sqlite_connection.execute(select_query, (email,))
        user_name = ""
        for user in user_record:
            password = user[0]
            user_name = user[2] 
        session['email'] = email
        update_query = """UPDATE user SET user_active = ? WHERE user_email = ?;"""
        update_query_data = (1, email)
        sqlite_connection.execute(update_query, update_query_data)
        sqlite_connection.commit()
        return redirect(url_for("user_mail_bp.see_inbox"))

@forms_bp.route('/validLogin/<user_email>/<user_password>', methods = ["POST"])
def auto_redirect(user_email, user_password):
    print(user_email)
    print(user_password)
    if check_user_exist(user_email, user_password):
        session['email'] = user_email
        session['password'] = user_password
        sqlite_connection = sqlite3.connect("MAIL_DB.db")
        update_query = """UPDATE user SET user_active = ?;"""
        sqlite_connection.execute(update_query, (1,))
        sqlite_connection.commit()
        sqlite_connection.close()
        success_message = f"Welcome Back {get_user_name(user_email)}"
        flash(success_message)
        return render_template("Forms/userPage.html",user_name = get_user_name(user_email))


@forms_bp.route('/ValidationRegistration',methods = ['POST']) #Creating User
def Validation():
    if request.method == 'POST':

        name = request.form['name']
        password = bcrypt.generate_password_hash(request.form['password']).decode("UTF-8")
        email = request.form['email']
        gender = request.form['gender']
        date_of_birth = request.form['dateOfBirth']
        city = request.form['city']
        country = request.form['country']
        contact = request.form['contact']
        account_creation_date = datetime.datetime.now()

        sqlite_connection = sqlite3.connect('Mail_DB.db')

        data_query = """INSERT INTO user (user_name, user_email, user_password, user_gender, user_date_of_birth,
                         user_city, user_country, user_contact, user_account_creation_date) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?); """
        user_data = (name, email, password,
        gender, date_of_birth, city, country,
        contact, account_creation_date)

        sqlite_connection.execute(data_query, user_data)
        sqlite_connection.commit()
        sqlite_connection.close()

        user_record = {
                       "name": name,
                       "email": email,
                       "password": password,
                       "gender": gender,
                       "date_of_birth": date_of_birth,
                       "city": city,
                       "country": country,
                       "contact": contact,
                       "account_creation_date": account_creation_date
                       }
             
        session['name'] = name
        session['email'] = email
        session['password'] = password
        return redirect(url_for("user_mail_bp.see_inbox"))
    else:
        return '<h1>Failed</h1>'     

