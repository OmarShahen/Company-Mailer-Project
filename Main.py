from flask import *
from admin import admin
from User import user
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "Shahen"
allUsers = []
adminOfApplication = admin('omar','omarredaelsayedmohamed@gmail.com','admin123','male','6/6/2000','Alexandria','Egypt','01065630331')

user1 = user('youssef','mailerfirstmailerlast@gmail.com','FirstLast11','Male','8/8/2006','Alexandria','Egypt','01265630331')
user1.set_appPassword(os.environ.get('FirstMailerPassword'))

user2 = user('Ahmed','mailersecondmailerlast@gmail.com','SecondLast11','Male','5/12/2006','Alexandria','Egypt','01006615471')
user2.set_appPassword(os.environ.get('SecondMailerPassword'))

user3 = user('Omar','omarredaelsayedmohamed@gmail.com','Shahen77','Male','6/6/2000','Alexandria','Egypt','01065630331')
user3.set_appPassword(os.environ.get('mailPassword'))

allUsers.append(user1)
allUsers.append(user2)
allUsers.append(user3)

@app.route('/')
@app.route('/LoginForm') #LoginForm
def loginFormPage():
    return render_template('LoginForm.html')

@app.route('/RegisterationForm') #Registration Form
def registerForm():
    return render_template('RegisterForm.html')

@app.route('/ValidLogin', methods = ['POST']) #Check Validation
def validLogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if adminOfApplication.get_password() == password and adminOfApplication.get_email() == email:
            session['email'] = email
            session['password'] = password
            return render_template('admin.html', adminName = adminOfApplication.get_name().upper(),allUsers = allUsers)
        
        for user in allUsers: 
            if user.get_email() == email and user.get_password() == password:
                session['name'] = user.get_name()
                session['email'] = email
                session['password'] = password
                session['appPassword'] = user.get_appPassword()
                user.set_active_online()
                return render_template("userPage.html",user = user)
      
@app.route('/ValidationRegistration',methods = ['POST']) #Creating User
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
        return render_template("userPage.html",user = userObject)
    else:
        return '<h1>Failed</h1>'

@app.route('/View profile')
def view_profile():
    for user in allUsers:
        if user.get_email() == session['email'] and user.get_password() == session['password']:
            return render_template('ViewProfile.html',user = user)

@app.route('/EditProfileForm', methods = ['POST','GET'])
def set_new_attributes():
    for user in allUsers:
        if user.get_password() == session['password'] and user.get_email() == session['email']:
            return render_template("editProfileForm.html", user = user)

@app.route('/Edited' , methods = ['POST'])
def edit_profile():

    if request.method == "POST":
        new_name = request.form['user_name']
        new_email = request.form['user_email']
        new_password = request.form['user_password']
        new_appPassword = request.form['user_appPassword']
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
                user.set_appPassword(new_appPassword)
                user.set_gender(new_gender)
                user.set_dateOfBirth(new_dateOfBirth)
                user.set_city(new_city)
                user.set_country(new_country)
                user.set_contact(new_contact)
                return "<h1>Edited Successfully</h1>"
        return "<h1>Does not Exist</h1>"

@app.route('/logout')
def logout():

    for user in allUsers:
        if session['email'] == user.get_email() and session['password'] == user.get_password():
            session.pop('name',None)
            session.pop('email',None)
            session.pop('password',None)
            session.pop('appPassword',None)
            user.set_active_offline()
            return render_template('logout.html')
    
@app.route('/composeEmail')
def composeEmail():
    return render_template('composeEmail.html',userName = session['email'])

@app.route('/sending_mail', methods = ['POST'])
def sendingMail():

    if request.method == "POST":

        sender_name = session['name']
        sender_mail = session['email']
        receiver_mail = request.form['reciever']
        mail_subject = request.form['subject']
        mail_body = request.form['mailInfo'].strip()

        email = {
                 "sender_name": sender_name,
                 "sender_mail": sender_mail,
                 "receiver_mail": receiver_mail,
                 "subject": mail_subject,
                 "body": mail_body
                }

        for user in allUsers:
            if user.get_email() == session['email']:
                user.add_to_outbox(email)       
            if user.get_email() == receiver_mail:
                user.add_inbox(email)
                
        return redirect(url_for('composeEmail'))
        

@app.route("/outbox")
def see_sent_mails():
    for user in allUsers:
        if user.get_email() == session['email']:
            return render_template("outbox.html", outbox_mails = user.get_all_outbox()) 

@app.route("/inbox")
def see_inbox():
    for user in allUsers:
        if user.get_email() == session["email"]:
            return render_template("inbox.html", inbox_mails = user.get_all_inbox())


@app.route("/allUsers")
def view_all_users():
    
    return render_template("allUsers.html", allUsers = allUsers)

















if __name__ == "__main__":
    app.run(debug = True)