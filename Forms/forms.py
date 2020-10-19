from flask import Blueprint, render_template, session, request, redirect, url_for, flash, jsonify, current_app
from admin import admin
from creating_users import allUsers, adminOfApplication
import sqlite3
import datetime
from flask_bcrypt import Bcrypt
import json
import smtplib, ssl
import os
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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


def phone_number_validator(phone_number):
    sqlite_connection = sqlite3.connect("MAIL_DB.db")
    select_users_phones_query = "SELECT user_contact FROM user;"
    select_admins_phones_query = "SELECT admin_phone FROM admin;"
    select_waiting_users_phones_query = "SELECT user_contact FROM waiting_list;"
    db_users_phones = sqlite_connection.execute(select_users_phones_query)
    db_admins_phones = sqlite_connection.execute(select_admins_phones_query)
    db_waiting_phones = sqlite_connection.execute(select_waiting_users_phones_query)
    all_phones = []
    for phone in db_users_phones:
        all_phones.append(phone[0])
    for phone in db_admins_phones:
        all_phones.append(phone[0])
    for phone in db_waiting_phones:
        all_phones.append(phone[0])

    for phone in all_phones:
        if phone_number == str(phone):
            return False
    return True

def activate_verfication_code(user_email, verfication_code):
    sqlite_connection = sqlite3.connect("MAIL_DB.db")
    insert_code_query = """INSERT INTO verfication_code(user_email, verfication_code, birth_date)
                            VALUES(?, ?, ?);"""
    values = (user_email, verfication_code, datetime.datetime.now())
    sqlite_connection.execute(insert_code_query, values)
    sqlite_connection.commit()
    sqlite_connection.close()
    return

def get_verfication_code_id(verfication_code):

    sqlite_connection = sqlite3.connect("MAIL_DB.db")
    select_query = "SELECT verfication_id FROM verfication_code WHERE verfication_code = ?;"
    db_ver_code = sqlite_connection.execute(select_query, (verfication_code,))
    verfication_id = 0
    for ver_id in db_ver_code:
        verfication_id = ver_id[0]
    sqlite_connection.close()
    print(verfication_id)
    return verfication_id
         
def return_date_formate(date):
    date_str_format = "%Y-%m-%d %H:%M:%S.%f"
    return datetime.datetime.strptime(date, date_str_format)




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
    
    select_users_mails_query = """SELECT user_email FROM user;"""
    select_admins_mails_query = """SELECT admin_email FROM admin;"""
    select_waiting_users_mails_query = """SELECT user_email FROM waiting_list;"""
    db_users_mails = sqlite_connection.execute(select_users_mails_query)
    db_admins_mails = sqlite_connection.execute(select_admins_mails_query)
    db_waiting_mails = sqlite_connection.execute(select_waiting_users_mails_query)
    all_mails = []
    for mail in db_users_mails:
        all_mails.append(mail[0])
    for mail in db_admins_mails:
        all_mails.append(mail[0])
    for mail in db_waiting_mails:
        all_mails.append(mail[0])

    for mail in all_mails:
        if input_mail.split("@")[0] == mail.split("@")[0]:
            response_message = {"message": "this mail is taken", "valid": False}
            return jsonify(response_message)
    response_message = {"message": "valid mail name", "valid": True}
    return jsonify(response_message)

@forms_bp.route("/phone-number/validator/<phone_number>")
def phone_validator(phone_number):
    valid = phone_number_validator(phone_number)
    response_message = {}
    if valid == True:
        response_message["valid"] = True
        return jsonify(response_message)
    else:
        response_message["valid"] = False
        response_message["message"] = "this number is taken"
        return jsonify(response_message)



@forms_bp.route("/forgot-password", methods = ["POST"])
def forgot_password():
    verfication_code = random.randrange(10000, 100000)
    message = MIMEMultipart("alternative")
    message["Subject"] = "Verfication Code"
    message["To"] = request.form.get("userFmail")
    message["From"] = current_app.config["APP_MAIL"]
    text_message = "Your Verfication Code: " + str(verfication_code)
    html_message = f"""<html>
    <body>
        <p>Your verfication code: <strong>{verfication_code}</strong>
    </body></html>"""
    part1 = MIMEText(text_message, "plain")
    part2 = MIMEText(html_message, "html")
    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", current_app.config["APP_PORT"], context = context) as server:
            server.login(current_app.config["APP_MAIL"], current_app.config["APP_MAIL_PASSWORD"])
            server.sendmail(current_app.config["APP_MAIL"], request.form.get("userFmail"),message.as_string())
            activate_verfication_code(request.form.get("userFmail"), verfication_code)
    except Exception:
        flash("Error occured! please check your internet connection", "gmail_error")
        return redirect(url_for("forms_bp.login_form_page"))
    return render_template("Forms/verficationCode.html", user_mail = request.form.get("userFmail"), ver_id = get_verfication_code_id(verfication_code))
    
@forms_bp.route("/resend-verfication-code/<receiver_mail>")
def resend_verfication_code(receiver_mail):
    verfication_code = random.randrange(10000, 100000)
    message = MIMEMultipart("alternative")
    message["Subject"] = "Verfication Code"
    message["To"] = receiver_mail
    message["From"] = current_app.config["APP_MAIL"]
    text_message = "Your Verfication Code: " + str(verfication_code)
    html_message = f"""<html>
    <body>
        <p>Your verfication code: <strong>{verfication_code}</strong>
    </body></html>"""
    part1 = MIMEText(text_message, "plain")
    part2 = MIMEText(html_message, "html")
    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", current_app.config["APP_PORT"], context = context) as server:
        server.login(current_app.config["APP_MAIL"], current_app.config["APP_MAIL_PASSWORD"])
        server.sendmail(current_app.config["APP_MAIL"], receiver_mail, message.as_string())
    activate_verfication_code(receiver_mail, verfication_code)
    return render_template("Forms/verficationCode.html", user_mail = receiver_mail, ver_id = get_verfication_code_id(verfication_code))

@forms_bp.route("/verfiy-code/<user_mail>/<ver_id>", methods = ["POST"])
def verfiy_code(user_mail, ver_id):
    sqlite_connection = sqlite3.connect("MAIL_DB.db")
    select_ver_code_query = """SELECT verfication_code, birth_date FROM verfication_code WHERE verfication_id = ?;"""
    db_ver_data = sqlite_connection.execute(select_ver_code_query, (ver_id,))
    ver_code = {}
    for ver_data in db_ver_data:
        ver_code["verfication_code"] = ver_data[0]
        ver_code["birth_date"] = return_date_formate(ver_data[1])
    date_difference = datetime.datetime.now() - ver_code["birth_date"]
    
    if ver_code["verfication_code"] != int(request.form.get("verficationCodeField")) or date_difference.seconds > 60:
        sqlite_connection.close()
        return redirect(url_for("forms_bp.verfication_code_error", user_mail = user_mail))   
    sqlite_connection.close()
    return render_template("Forms/changePassword.html", user_mail = user_mail)

@forms_bp.route("/Invalid-verfication-code/<user_mail>")
def verfication_code_error(user_mail):
    error_message = "Invalid verfication code"
    return render_template("Forms/verficationCodeError.html", error_message = error_message, user_mail = user_mail)
    





@forms_bp.route("/change-user-password/<user_mail>", methods = ["POST"])
def change_user_password(user_mail):
    sqlite_connection = sqlite3.connect("MAIL_DB.db")
    update_password_query = "UPDATE user SET user_password = ? WHERE user_email = ?;"
    new_hashed_password = bcrypt.generate_password_hash(request.form.get("newPassword")).decode("UTF-8")
    update_password_values = (new_hashed_password, user_mail)
    sqlite_connection.execute(update_password_query, update_password_values)
    sqlite_connection.commit()
    sqlite_connection.close()
    session["email"] = user_mail
    return redirect(url_for('user_mail_bp.see_inbox'))

    



