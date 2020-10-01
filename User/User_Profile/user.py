from flask import Blueprint, render_template, session, request, redirect, url_for, flash, abort
from creating_users import allUsers, adminOfApplication
import sqlite3
from Forms.forms import bcrypt

user_profile_bp = Blueprint('user_profile_bp', __name__, template_folder = 'templates', static_folder = 'static')


@user_profile_bp.route('/View profile')
def view_profile():
    user_email = session['email']

    sqlite_connection = sqlite3.connect('Mail_DB.db')
    select_user_query = """SELECT user_id, user_name, user_email, user_gender
                            ,user_date_of_birth, user_city, user_country, user_contact
                            , user_account_creation_date FROM user
                            WHERE user_email = ?;"""
    select_user_query_data = (user_email,)
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

    sqlite_connection.close()
    return render_template("User_Profile/ViewProfile.html", user = user_record)

@user_profile_bp.route('/EditProfileForm')
def edit_profile_form():
    sqlite_connection = sqlite3.connect('Mail_DB.db')
    select_user_query = """SELECT * FROM user WHERE user_email = ?;"""
    select_user_query_data = (session['email'],)
    user_data = sqlite_connection.execute(select_user_query, select_user_query_data)
    user_record = {}
    for data in user_data:
        user_record['NAME'] = data[1]
        user_record['EMAIL'] = data[2]
        user_record['DATE_OF_BIRTH'] = data[5]
        user_record['CITY'] = data[6]
        user_record['COUNTRY'] = data[7]
        user_record['CONTACT'] = data[8]
        user_record['ACCOUNT_CREATRION_DATE'] = data[9]
    sqlite_connection.close()
    return render_template('User_Profile/editProfileForm.html', user = user_record)

@user_profile_bp.route("/Editing", methods = ['POST'])
def edit_profile():

    new_name = request.form['user_name']
    new_email = request.form['user_email']
    new_dateOfBirth = request.form['user_birthDate']
    new_city = request.form['user_city']
    new_country = request.form['user_country']
    new_contact = request.form['user_contact']
    

    sqlite_connection  = sqlite3.connect('Mail_DB.db')
    user_update_query = """UPDATE user SET user_name = ?, user_email = ?, user_date_of_birth = ?,
                           user_city = ?, user_country = ?, user_contact = ?  WHERE user_email = ?;"""
    user_update_query_data = (new_name, new_email, new_dateOfBirth, new_city, new_country, new_contact, session['email'])
    sqlite_connection.execute(user_update_query, user_update_query_data)
    sqlite_connection.commit()
    sqlite_connection.close()
    flash("Successfully!!!", "success")
    return redirect(url_for("user_profile_bp.edit_profile_form"))
 

@user_profile_bp.route('/All-Users')
def view_all_users():  

    sqlite_connection = sqlite3.connect('Mail_DB.db')
    select_allusers_query = """SELECT user_id , user_name, user_email FROM user;"""
    allUsers = sqlite_connection.execute(select_allusers_query).fetchall()
    sqlite_connection.close()
    return render_template("User_Profile/allUsers.html", allUsers = allUsers)
   


@user_profile_bp.route('/logout')
def logout():
    sqlite_connection = sqlite3.connect('Mail_DB.db')
    user_update_query = """UPDATE user SET user_active = ? WHERE user_email = ?;"""
    user_update_query_data = (0, session['email'])
    sqlite_connection.execute(user_update_query, user_update_query_data)
    sqlite_connection.commit()
    sqlite_connection.close()
    session.pop('email', None)
    return redirect(url_for("forms_bp.login_form_page"))
 

@user_profile_bp.route('/delete-account', methods = ['DELETE'])
def delete_account():

    sqlite_connection = sqlite3.connect('Mail_DB.db')
    user_delete_query = """DELETE FROM user WHERE user_email = ? AND user_password = ?;"""
    sqlite_connection.execute(user_delete_query, (session['email'], session['password']))
    sqlite_connection.commit()
    sqlite_connection.close()
    session.pop('email', None)
    session.pop('password', None)
    return "<h1>Your Account is Deleted successfully</h1>"





    