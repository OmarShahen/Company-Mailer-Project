from flask import Blueprint, request, render_template, url_for, jsonify, flash, redirect
import sqlite3
from Forms.forms import bcrypt
admin_bp = Blueprint("admin_bp", __name__, template_folder = "templates")

@admin_bp.route("/admin/main-page")
def admin_page():
    sqlite_connection = sqlite3.connect("MAIL_DB.db")

    check_unauthorized_query = """SELECT user_email FROM unauthorize;"""
    db_unauthorized_mails = sqlite_connection.execute(check_unauthorized_query)
    un_authorized_mails = []
    for mail in db_unauthorized_mails:
        un_authorized_mails.append(mail[0])

    select_all_users = """SELECT user_id, user_name, user_email, user_active FROM user;"""
    db_all_users = sqlite_connection.execute(select_all_users)
    user_data = {}
    all_users = []
    for user in db_all_users:
        user_data["user_id"] = user[0]
        user_data["user_name"] = user[1]
        user_data["user_email"] = user[2]
        user_data["user_status"] = user[3]
        user_data["user_authorized"] = True
        for mail in un_authorized_mails:
            if mail == user[2]:
                user_data["user_authorized"] = False
                break
        all_users.append(user_data)
        user_data = {}

    return render_template("admin_templates/admin.html", all_users = all_users)


@admin_bp.route("/admin/unauthorize/<string:user_mail>", methods = ["GET"])
def admin_unauthorize(user_mail):
    sqlite_connection = sqlite3.connect("MAIL_DB.db")
    insert_mail_query = """INSERT INTO unauthorize (user_email) VALUES(?);"""
    sqlite_connection.execute(insert_mail_query, (user_mail,))
    sqlite_connection.commit()
    sqlite_connection.close()
    flash("unauthorized successfully", "unauthorize")
    return redirect(url_for("admin_bp.admin_page"))

@admin_bp.route("/admin/authorize/<string:user_mail>", methods = ["GET"])
def admin_authorize(user_mail):
    sqlite_connection = sqlite3.connect("MAIL_DB.db")
    remove_mail_query = """DELETE FROM unauthorize WHERE user_email = ?;"""
    sqlite_connection.execute(remove_mail_query, (user_mail,))
    sqlite_connection.commit()
    sqlite_connection.close()
    flash("authorized successfully", "authorize")
    return redirect(url_for("admin_bp.admin_page"))

    
@admin_bp.route("/admin/user-activity", methods = ["GET"])
def check_status():
    sqlite_connection = sqlite3.connect("MAIL_DB.db")
    select_status_query = """SELECT user_active FROM user;"""
    db_users_activity = sqlite_connection.execute(select_status_query)
    users_activity = []
    for status in db_users_activity:
        users_activity.append(status[0])
    return jsonify(users_activity)



@admin_bp.route("/admin/add-admin", methods = ["POST"])
def add_admin():
    admin_mail = request.form.get("adminMail")
    admin_password = request.form.get("adminPassword")
    admin_phone = request.form.get("adminPhone")  
    admin_password = bcrypt.generate_password_hash(admin_password).decode("UTF-8")
    sqlite_connection = sqlite3.connect("MAIL_DB.db")
    add_admin_query = """INSERT INTO admin (admin_email, admin_password, admin_phone) VALUES(?, ?, ?);"""
    sqlite_connection.execute(add_admin_query, (admin_mail, admin_password, admin_phone))
    sqlite_connection.commit()
    sqlite_connection.close()
    return redirect(url_for("admin_bp.admin_page")) 

@admin_bp.route("/admin/emails-validator/<input_mail>")
def email_validator(input_mail):
    if "@" not in input_mail:
        input_mail = input_mail + "@"
    sqlite_connection = sqlite3.connect("MAIL_DB.db")
    select_all_mails_query = """SELECT admin_email FROM admin;"""
    db_all_mails = sqlite_connection.execute(select_all_mails_query)
    for mail in db_all_mails:
        if input_mail.split("@")[0] == mail[0].split("@")[0]:
            response_message = {"message": "This mail is taken", "valid": False}
            return jsonify(response_message)
    response_message = {"message": "valid mail name", "valid": True}
    return jsonify(response_message)

@admin_bp.route("/admin/phone-number-validator/<phone_number>")
def phone_validator(phone_number):
    sqlite_connection = sqlite3.connect("MAIL_DB.db")
    select_phones_query = """SELECT admin_phone FROM admin;"""
    db_phone_numbers = sqlite_connection.execute(select_phones_query)
    for phone in db_phone_numbers:
        if phone_number == phone[0]:
            return jsonify("This number is taken")
    return jsonify("")
