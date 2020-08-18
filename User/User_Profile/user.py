from flask import Blueprint, render_template, session, request, redirect, url_for
from creating_users import allUsers, adminOfApplication
import sqlite3

user_profile_bp = Blueprint('user_profile_bp', __name__, template_folder = 'templates', static_folder = 'static')


@user_profile_bp.route('/View profile')
def view_profile():
    for user in allUsers:
        if user.get_email() == session['email'] and user.get_password() == session['password']:
            return render_template('User_Profile/ViewProfile.html',user = user)


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



        

 