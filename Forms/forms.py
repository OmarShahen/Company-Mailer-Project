from flask import Blueprint, render_template, session, request, redirect, url_for
from admin import admin
from user import user
from creating_users import allUsers, adminOfApplication
import sqlite3

forms_bp = Blueprint('forms_bp', __name__, template_folder = 'templates', static_folder = 'static')




@forms_bp.route('/')
@forms_bp.route('/LoginForm') #LoginForm
def loginFormPage():
    return render_template('Forms/LoginForm.html')

@forms_bp.route('/RegisterationForm') #Registration Form
def registerForm():
    return render_template('Forms/RegisterForm.html')


@forms_bp.route('/ValidLogin', methods = ['POST']) #Check Validation
def validLogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if adminOfApplication.get_password() == password and adminOfApplication.get_email() == email:
            session['email'] = email
            session['password'] = password
            return render_template('Forms/admin.html', adminName = adminOfApplication.get_name().upper(),allUsers = allUsers)
        
        sqlite_connection = sqlite3.connect('MAIL_DB.db')
        select_query = """SELECT PASSWORD, EMAIL, NAME FROM USER WHERE PASSWORD = ? AND EMAIL = ?;"""
        users_records = sqlite_connection.execute(select_query, (password, email)).fetchall()
        
        if len(users_records) == 0:
            return "<h1>The User does not exist</h1>"
        user_name = ""
        for user in users_records:
            user_name = user[2] 
        session['email'] = email
        session['password'] = password
        update_query = """UPDATE USER SET ACTIVE = 1 WHERE PASSWORD = ?
                          AND EMAIL = ?;"""
        update_query_data = (password, email)
        sqlite_connection.execute(update_query, update_query_data)
        return render_template("Forms/userPage.html",user_name = user_name)

@forms_bp.route('/ValidationRegistration',methods = ['POST']) #Creating User
def Validation():
    if request.method == 'POST':

        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        gender = request.form['gender']
        dateOfBirth = request.form['dateOfBirth']
        city = request.form['city']
        country = request.form['country']
        contact = request.form['contact']

        userObject = user(name,email,password,gender,dateOfBirth,city,country,contact)
        allUsers.append(userObject)

        sqlite_connection = sqlite3.connect('Mail_DB.db')

        data_query = """INSERT INTO USER (NAME, EMAIL, PASSWORD, GENDER, DATE_OF_BIRTH, CITY, COUNTRY,
                         CONTACT, ACCOUNT_CREATION_DATE) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?); """
        user_data = (name, email, password, gender, dateOfBirth, city, country, contact, userObject.get_account_creation_date())
        sqlite_connection.execute(data_query, user_data)
        sqlite_connection.commit()
        sqlite_connection.close()
        
        
        session['name'] = name
        session['email'] = email
        session['password'] = password
        return render_template("Forms/userPage.html",user = userObject)
    else:
        return '<h1>Failed</h1>'     
