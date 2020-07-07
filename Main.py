from flask import *
from admin import admin
from User import user
import smtplib, ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
import send_mail
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "Shahen"
allUsers = []
adminOfApplication = admin('omar','omarredaelsayedmohamed@gmail.com','admin123','male','6/6/2000','Alexandria','Egypt','01065630331')

user1 = user('youssef','mailerfirstmailerlast@gmail.com','FirstLast11','male','8/8/2006','Alexandria','Egypt','01265630331')
user1.set_appPassword(os.environ.get('FirstMailerPassword'))

user2 = user('Ahmed','mailersecondmailerlast@gmail.com','SecondLast11','male','5/12/2006','Alexandria','Egypt','01006615471')
user2.set_appPassword(os.environ.get('SecondMailerPassword'))

user3 = user('Omar','omarredaelsayedmohamed@gmail.com','Shahen77','male','6/6/2000','Alexandria','Egypt','01065630331')
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

@app.route('/composeEmail/',methods = ['POST'])
def sendingMail():

    if request.method == 'POST':
        sender = session['email']
        sender_password  = session['appPassword']
        receiver = request.form['reciever']
        subject = request.form['subject']
        body = request.form['mailInfo']
        if request.files:
            sender_file = request.files["user_file"]
            file_name = secure_filename(sender_file.filename)
            root_path = "E:\\Mailer\\Users"
            main_path = os.path.join(root_path, session['name'], "sent")
            print(main_path)
            try:
                os.makedirs(main_path)
                print("The Directry is created and saved")
            except OSError as error:
                print("The Directory already Exist")
            file_location = os.path.join(main_path, file_name)
            sender_file.save(file_location)
            send_mail.send_mail_attachment(sender, sender_password, receiver, subject, body, file_location, file_name)
            print("Saved Successfully")
        send_mail.send_mail(sender, sender_password, receiver, subject, body)


        return "<h1>Sent Successfully</h1>"#send_mail.send_mail(sender, sender_password,receiver,subject,body,file_attachment)

        



      







if __name__ == "__main__":
    app.run(debug = True)