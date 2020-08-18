from flask import Blueprint, request, jsonify, session, render_template
from creating_users import allUsers, user
import sqlite3


mail_api = Blueprint('mail_api', __name__)

@mail_api.route('/ValidationRegistration',methods = ['POST']) #Creating User
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



