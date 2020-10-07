from flask import Blueprint, request, render_template, url_for, jsonify, flash, redirect
import sqlite3

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

    
