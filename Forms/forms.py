from flask import Blueprint, render_template, session, request, redirect, url_for, flash, jsonify
from admin import admin
from creating_users import allUsers, adminOfApplication
import sqlite3
import datetime
from flask_bcrypt import Bcrypt
import json



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

def check_admin_exist(user_email, user_password):
    sqlite_connection = sqlite3.connect('MAIL_DB.db')
    select_query = """SELECT admin_email, admin_password FROM admin;"""
    db_admin_records = sqlite_connection.execute(select_query).fetchall()
    sqlite_connection.close()
    if len(db_admin_records) == 0:
        return False
    for admin in db_admin_records:
        print(user_email, " == ", admin[0])
        print("Encryption result: ", bcrypt.check_password_hash(admin[1], user_password))
        if user_email == admin[0] and bcrypt.check_password_hash(admin[1], user_password):
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
        
        
        if check_admin_exist(email, password):
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


@forms_bp.route('/waiting-page/<user_name>')
def waiting_page(user_name):
    return render_template("Forms/waitingPage.html", user_name = user_name)

@forms_bp.route('/Validate-Registration', methods = ["POST"]) #Creating User
def validation():

    sqlite_connection = sqlite3.connect('Mail_DB.db')

    select_mails_query = """SELECT user_email FROM user;"""
    db_all_users_emails = sqlite_connection.execute(select_mails_query)
    for mail in db_all_users_emails:
        if request.form['email'] == mail[0]:
            flash("This email is already taken", "email_error")
            return redirect(url_for('forms_bp.registerForm'))

    name = request.form['name']
    password = bcrypt.generate_password_hash(request.form['password']).decode("UTF-8")
    email = request.form['email']
    gender = request.form['gender']
    date_of_birth = request.form['dateOfBirth']
    city = request.form['city']
    country = request.form['country']
    contact = request.form['contact']
    account_creation_date = datetime.datetime.now()

    data_query = """INSERT INTO waiting_list (user_name, user_email, user_password, user_gender, user_date_of_birth,
                    user_city, user_country, user_contact, user_account_creation_date) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?); """
    user_data = (name, email, password,
    gender, date_of_birth, city, country,
    contact, account_creation_date)

    sqlite_connection.execute(data_query, user_data)
    sqlite_connection.commit()
    sqlite_connection.close()

    return redirect(url_for('forms_bp.waiting_page', user_name = name))

@forms_bp.route("/emails-validator/<input_mail>")
def email_validator(input_mail):
    if "@" not in input_mail:
        input_mail = input_mail + "@"
    print(input_mail)
    sqlite_connection = sqlite3.connect("MAIL_DB.db")
    select_all_mails_query = """SELECT user_email FROM user;"""
    db_all_mails = sqlite_connection.execute(select_all_mails_query)
    for mail in db_all_mails:

        if input_mail.split("@")[0] == mail[0].split("@")[0]:
            response_message = {"message": "this mail is taken", "valid": False}
            return jsonify(response_message)
    response_message = {"message": "valid mail name", "valid": True}
    return jsonify(response_message)

@forms_bp.route("/forgot-password", methods = ["POST"])
def forgot_password():
    user_email = request.form.get('userFmail')
    print(user_email)
    return "DONE"
    



