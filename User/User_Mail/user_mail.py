from flask import Blueprint, render_template, session, request, redirect, url_for
from admin import admin
from user import user
from creating_users import allUsers, adminOfApplication

user_mail_bp = Blueprint('user_mail_bp', __name__, template_folder = 'templates', static_folder = 'static')


@user_mail_bp.route('/composeEmail')
def composeEmail():
    return render_template('User_Mail/composeEmail.html',userName = session['email'])


@user_mail_bp.route('/sending_mail', methods = ['POST'])
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
                
        return redirect(url_for('user_mail_bp.composeEmail'))


@user_mail_bp.route("/outbox")
def see_sent_mails():
    for user in allUsers:
        if user.get_email() == session['email']:
            return render_template("User_Mail/outbox.html", outbox_mails = user.get_all_outbox()) 


@user_mail_bp.route("/inbox")
def see_inbox():
    for user in allUsers:
        if user.get_email() == session["email"]:
            return render_template("User_Mail/inbox.html", inbox_mails = user.get_all_inbox())

