from flask import Blueprint, render_template, session, request, redirect, url_for, current_app, jsonify
from werkzeug.utils import secure_filename
import sqlite3
import os
from datetime import datetime
import validator

def get_user_id(user_email):
    sqlite_connection = sqlite3.connect('MAIL_DB.db')
    select_user_query = """SELECT user_id FROM user WHERE user_email = ?;"""
    select_user_query_data = (user_email,)
    user_record = sqlite_connection.execute(select_user_query, select_user_query_data)
    user_id = 0
    for data in user_record:
        user_id = data[0]
    sqlite_connection.close()
    return user_id

def get_user_email(user_id):
    sqlite_connection = sqlite3.connect('MAIL_DB.db')
    select_user_query = """SELECT user_email FROM user WHERE user_id = ?;"""
    select_user_query_data = (user_id,)
    user_record = sqlite_connection.execute(select_user_query, select_user_query_data)
    user_email = "" 
    for data in user_record:
        user_email = data[0]
    sqlite_connection.close()
    return user_email
        

def check_attachment_exist(mail_id):
    sqlite_connection = sqlite3.connect('MAIL_DB.db')
    search_file_query = """SELECT * FROM attachment WHERE mail_id = ?;"""
    search_file_query_data = (mail_id,)
    file_list = sqlite_connection.execute(search_file_query, search_file_query_data).fetchall()
    if len(file_list) == 0:
        sqlite_connection.close()
        return False
    else:
        sqlite_connection.close()
        return True

def get_attachments(mail_id):
    sqlite_connection = sqlite3.connect('MAIL_DB.db')
    select_attachment_query = """SELECT attachment_file FROM attachment WHERE mail_id = ?;"""
    mail_attachments = sqlite_connection.execute(select_attachment_query, (mail_id,))
    file_list = []
    for file in mail_attachments:
        file_list.append(file)
    sqlite_connection.close()
    return file_list


def check_files_numbers(files):
    for file in files:
        if file.filename == "":
            return False
    return True

def check_file_extension(files):
    for file in files:
        if '.' not in file.filename:
            return False
        splite_file = file.filename.split('.')
        print(splite_file)
        if splite_file[1].upper() not in current_app.config['ALLOWED_EXTENSIONS']:
            return False
    return True
    



user_mail_bp = Blueprint('user_mail_bp', __name__, template_folder = 'templates', static_folder = 'static/user_mail')


@user_mail_bp.route('/composeEmail')
def composeEmail():
    return render_template('User_Mail/composeEmail.html',userName = session['email'])


@user_mail_bp.route('/sending-mail', methods = ['POST', 'GET'])
def sendingMail():

    sender_mail = session['email']
    receiver_mail = request.form['reciever']
    mail_subject = request.form['subject']
    mail_body = request.form['mailInfo'].strip()

    sender_id = get_user_id(session['email'])
    receiver_id = get_user_id(receiver_mail)

    sqlite_connection = sqlite3.connect('MAIL_DB.db')
    sqlite_mail_query = """INSERT INTO mail (sender_id, receiver_id, mail_subject, mail_body, mail_date)
                            VALUES(?, ?, ?, ?, ?);"""
    sqlite_mail_query_data = (sender_id, receiver_id, mail_subject, mail_body, datetime.now())
    sqlite_connection.execute(sqlite_mail_query, sqlite_mail_query_data)

    sqlite_select_query = """SELECT mail_id FROM mail WHERE sender_id = ? AND receiver_id = ? ORDER BY mail_id DESC; """
    sqlite_select_query_data = (sender_id, receiver_id)
    mail_ids = sqlite_connection.execute(sqlite_select_query, sqlite_select_query_data)
    target_mail_id = None
    for id in mail_ids:
        target_mail_id = id[0]
        break
    user_files = None

    if check_files_numbers(request.files.getlist('user_files')):

        user_files = request.files.getlist('user_files')
        if check_file_extension(user_files) == False:
            return "not allowed extension"

        os.makedirs(current_app.config['USER_ATTACHMENTS'], exist_ok = True)
        for user_file in user_files:
            print(user_file.file)
            file_name = secure_filename(user_file.filename)
            user_file.save(os.path.join(current_app.config['USER_ATTACHMENTS'], file_name))
            save_attachment_query = """INSERT INTO attachment(mail_id, sender_id, receiver_id, attachment_file)
                                        VALUES(?, ?, ?, ?);"""
            save_attachment_query_data = (target_mail_id, sender_id, receiver_id, user_file.filename)
            sqlite_connection.execute(save_attachment_query, save_attachment_query_data)
    sqlite_connection.commit()
    sqlite_connection.close()


    return redirect(url_for('user_mail_bp.composeEmail'))



@user_mail_bp.route("/outbox")
def see_sent_mails():
    sqlite_connection = sqlite3.connect('MAIL_DB.db')
    sender_id = get_user_id(session['email'])
    select_sender_query = """SELECT * FROM mail WHERE sender_id = ? ORDER BY  mail_id DESC;"""
    user_outbox = sqlite_connection.execute(select_sender_query, (sender_id,))
    outbox = []
    mail_data = {}
    for mail in user_outbox:
        mail_data['mail_id'] = mail[0]
        mail_data['sender_id'] = mail[1]
        mail_data['receiver_id'] = mail[2]
        mail_data['receiver_mail'] = get_user_email(mail[2])
        mail_data['mail_subject'] = mail[3]
        mail_data['mail_body'] = mail[4]
        mail_data['mail_date'] = mail[5]
        mail_data['mail_seen'] = mail[6]

        if check_attachment_exist(mail[0]):
            mail_data['mail_attachments'] = get_attachments(mail[0])

        outbox.append(mail_data)
        mail_data = {}
    sqlite_connection.close()
    return render_template("User_Mail/outbox.html", outbox_mails = outbox) 


@user_mail_bp.route("/inbox")
def see_inbox():
    sqlite_connection = sqlite3.connect('MAIL_DB.db')

    user_id = get_user_id(session['email'])

    get_inbox_query = """SELECT * FROM mail WHERE receiver_id = ? ORDER BY mail_id DESC;"""
    get_inbox_query_data = (user_id,)
    user_inbox = sqlite_connection.execute(get_inbox_query, get_inbox_query_data)
    mail_data = {}
    inbox = []
    for mail in user_inbox:
        mail_data['mail_id'] = mail[0]
        mail_data['sender_id'] = mail[1]
        mail_data['sender_mail'] = get_user_email(mail[1])
        mail_data['receiver_id'] = mail[2]
        mail_data['receiver_mail'] = get_user_email(mail[2])
        mail_data['mail_subject'] = mail[3]
        mail_data['mail_body'] = mail[4]
        mail_data['mail_date'] = mail[5]
        print(mail_data['mail_date'])
        print(type(mail_data['mail_date']))
        mail_data['mail_seen'] = mail[6]

        if check_attachment_exist(mail[0]):
            mail_data['mail_attachments'] = get_attachments(mail[0])
        
        inbox.append(mail_data)

        mail_data = {}
    sqlite_connection.close()
    return render_template("User_Mail/inbox.html", inbox_mails = inbox)
