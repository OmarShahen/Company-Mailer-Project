from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from admin import admin
from creating_users import allUsers, adminOfApplication
import sqlite3
import datetime

forms_bp = Blueprint('forms_bp', __name__, template_folder = 'templates', static_folder = 'static')




@forms_bp.route('/')
@forms_bp.route('/LoginForm') #LoginForm
def login_form_page():
    return render_template('Forms/LoginForm.html')

@forms_bp.route('/RegisterationForm') #Registration Form
def registerForm():
    return render_template('Forms/RegisterForm.html')


@forms_bp.route('/ValidLogin', methods = ['POST']) #Check Validation
def valid_login():
    if request.method == 'POST':

        sqlite_connection = sqlite3.connect('MAIL_DB.db')

        email = request.form['email']
        password = request.form['password']
        if adminOfApplication.get_password() == password and adminOfApplication.get_email() == email:
            session['email'] = email
            session['password'] = password
            return render_template('Forms/admin.html', adminName = adminOfApplication.get_name().upper())
        
        select_query = """SELECT user_password, user_email, user_name FROM user WHERE user_password = ? AND user_email = ?;"""
        users_records = sqlite_connection.execute(select_query, (password, email)).fetchall()
        
        if len(users_records) == 0:
            flash("This Account doesnot Exist")
            return redirect(url_for("forms_bp.login_form_page"))
        user_name = ""
        for user in users_records:
            user_name = user[2] 
        session['email'] = email
        session['password'] = password
        update_query = """UPDATE user SET user_active = ? WHERE user_password = ?
                          AND user_email = ?;"""
        update_query_data = (1, password, email)
        sqlite_connection.execute(update_query, update_query_data)
        sqlite_connection.commit()
        success_message = f"Welcome Back {user_name}"
        flash(success_message)
        return render_template("Forms/userPage.html",user_name = user_name)

@forms_bp.route('/ValidationRegistration',methods = ['POST']) #Creating User
def Validation():
    if request.method == 'POST':

        name = request.form['name']
        password = request.form['password']
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
        return render_template('Forms/userPage.html', user_name = name)
    else:
        return '<h1>Failed</h1>'     
