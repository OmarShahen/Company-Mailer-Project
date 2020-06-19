from flask import *
from admin import admin
from User import user
import smtplib, ssl
import os


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
        port = 465
        context = ssl.create_default_context()
        sender_email = session['email']
        sender_password = session['appPassword']
        receiver_email = request.form['reciever']
        email_subject = request.form['subject']
        message_body = request.form['mailInfo'].strip()
        message = """from : %s \nto:%s\nsubject: %s\n\n%s"""%(sender_email,receiver_email,email_subject,message_body)
        

        
        

        print("sender email: ",sender_email)
        print("senderemail: ",session['email'])
        print("sender password: ",sender_password)
        print("sender password: ",session['appPassword'])
        print("receiver: ",request.form['reciever'])
        print("receiver: ",receiver_email)
        print("message: ",message.strip())
        print(type(message))
        with smtplib.SMTP_SSL("smtp.gmail.com",port,context = context) as server:
            server.login(sender_email,sender_password)
            server.sendmail(sender_email,receiver_email,message)
            return "<h1>Sent Successfully</h1>"



      







if __name__ == "__main__":
    app.run(debug = True)