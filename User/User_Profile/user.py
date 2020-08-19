from flask import Blueprint, render_template, session, request, redirect, url_for
from creating_users import allUsers, adminOfApplication
import sqlite3

user_profile_bp = Blueprint('user_profile_bp', __name__, template_folder = 'templates', static_folder = 'static')


@user_profile_bp.route('/View profile')
def view_profile():
    user_email = session['email']
    print("Session=", user_email)
    user_password = session['password']
    print("Session=", user_password)

    sqlite_connection = sqlite3.connect('Mail_DB.db')
    select_user_query = """SELECT ID, NAME, EMAIL, GENDER
                            ,DATE_OF_BIRTH, CITY, COUNTRY, CONTACT
                            , ACCOUNT_CREATION_DATE, ACTIVE FROM USER
                            WHERE EMAIL = ? AND PASSWORD = ?;"""
    select_user_query_data = (user_email, user_password)
    user_data = sqlite_connection.execute(select_user_query, select_user_query_data)
    user_record = {}
    for data in user_data:
        user_record['ID'] = data[0]
        user_record['NAME'] = data[1]
        user_record['EMAIL'] = data[2]
        user_record['GENDER'] = data[3]
        user_record['DATE_OF_BIRTH'] = data[4]
        user_record['CITY'] = data[5]
        user_record['COUNTRY'] = data[6]
        user_record['CONTACT'] = data[7]
        user_record['ACCOUNT_CREATION_DATE'] =  data[8]
        user_record['ACTIVE'] = data[9]

    sqlite_connection.close()
    return render_template("User_Profile/ViewProfile.html", user = user_record)

@user_profile_bp.route('/EditProfileForm', methods = ['POST','GET'])
def set_new_attributes():
    for user in allUsers:
        if user.get_password() == session['password'] and user.get_email() == session['email']:
            return render_template("User_Profile/editProfileForm.html", user = user)


@user_profile_bp.route('/Edited' , methods = ['POST'])
def edit_profile():

    if request.method == "POST":
        new_name = request.form['user_name']
        new_email = request.form['user_email']
        new_password = request.form['user_password']
        new_gender = request.form['user_gender']
        new_dateOfBirth = request.form['user_birthDate']
        new_city = request.form['user_city']
        new_country = request.form['user_country']
        new_contact = request.form['user_contact']

        for user in allUsers:
            if user.get_password() == session['password'] and user.get_email() == session['email']:
                user.set_name(new_name)
                user.set_email(new_email)
                user.set_password(new_password)
                user.set_gender(new_gender)
                user.set_dateOfBirth(new_dateOfBirth)
                user.set_city(new_city)
                user.set_country(new_country)
                user.set_contact(new_contact)
                return "<h1>Edited Successfully</h1>"
        return "<h1>Does not Exist</h1>"
 

@user_profile_bp.route('/allUsers')
def view_all_users():  
    sqlite_connection = sqlite3.connect('Mail_DB.db')
    select_allusers_query = """SELECT ID ,NAME, EMAIL FROM USER;"""
    allUsers = sqlite_connection.execute(select_allusers_query).fetchall()
    return render_template("User_Profile/allUsers.html", allUsers = allUsers)


@user_profile_bp.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('password', None)
    return render_template("User_Profile/logout.html")



        

 