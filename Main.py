from flask import *
from admin import admin
from User import user


app = Flask(__name__)
app.secret_key = "Shahen"
allUsers = []
adminOfApplication = admin('omar','omarredaelsayedmohamed@gmail.com','admin123','male','6/6/2000','Alexandria','Keshda','Egypt','01065630331')
allUsers.append(user('youssef','youssef@gmail.com','youssef77','male','8/8/2006','Alexandria','keshda','Egypt','01265630331'))
allUsers.append(user('Ahmed','ahmed@gmail.com','ahmed77','male','5/12/2006','Alexandria','Keshda','Egypt','01006615471'))


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
                return render_template("userPage.html",user = user)

    
    
               

@app.route('/ValidationRegistration',methods = ['POST']) #Creating User
def Validation():
    if request.method == 'POST':

        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        gender = request.form['gender']
        dateOfBirth = request.form['dateOfBirth']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        contact = request.form['contact']

        userObject = user(name,email,password,gender,dateOfBirth,city,state,country,contact)
        allUsers.append(userObject)
        return render_template("userPage.html",userName = name.upper())
    else:
        return '<h1>Failed</h1>'
    








if __name__ == "__main__":
    app.run(debug = True)