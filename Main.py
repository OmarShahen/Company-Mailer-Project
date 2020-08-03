from flask import *
from admin import admin
from user import user
import os
from werkzeug.utils import secure_filename
from Forms.forms import forms_bp
from User.User_Profile.user import user_profile_bp
from User.User_Mail.user_mail import user_mail_bp

app = Flask(__name__)
app.secret_key = "Shahen"


app.register_blueprint(forms_bp)
app.register_blueprint(user_profile_bp)
app.register_blueprint(user_mail_bp)

  

if __name__ == "__main__":
    app.run(debug = True)