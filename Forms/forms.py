from flask import Blueprint, render_template, session, request, redirect, url_for
from admin import admin
from user import user
from creating_users import allUsers, adminOfApplication

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
        
        for user in allUsers: 
            if user.get_email() == email and user.get_password() == password:
                session['name'] = user.get_name()
                session['email'] = email
                session['password'] = password
                session['appPassword'] = user.get_appPassword()
                user.set_active_online()
                return render_template("Forms/userPage.html",user = user)
      
@forms_bp.route('/ValidationRegistration',methods = ['POST']) #Creating User
def Validation():
    if request.method == 'POST':

        name = request.form['name']
        password = request.form['password']
        appPassword = request.form['appPassword']
        email = request.form['email']
        gender = request.form['gender']
        dateOfBirth = request.form['dateOfBirth']
        city = request.form['city']
        country = request.form['country']
        contact = request.form['contact']

        userObject = user(name,email,password,gender,dateOfBirth,city,country,contact)
        userObject.set_appPassword(appPassword)
        allUsers.append(userObject)
        session['name'] = name
        session['email'] == email
        session['password'] == password
        session['appPassword'] == appPassword
        return render_template("Forms/userPage.html",user = userObject)
    else:
        return '<h1>Failed</h1>'

