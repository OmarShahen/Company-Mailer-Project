from flask import Blueprint, request, render_template, url_for
import sqlite3

admin_bp = Blueprint("admin_bp", __name__, template_folder = "templates")

@admin_bp.route("/admin/main-page")
def admin_page():
    sqlite_connection = sqlite3.connect("MAIL_DB.db")
    select_all_users = """SELECT user_id, user_name, user_email, user_active FROM user;"""
    db_all_users = sqlite_connection.execute(select_all_users)
    user_data = {}
    all_users = []
    for user in db_all_users:
        user_data["user_id"] = user[0]
        user_data["user_name"] = user[1]
        user_data["user_email"] = user[2]
        user_data["user_status"] = user[3]
        all_users.append(user_data)
        user_data = {}
    return render_template("admin_templates/admin.html", all_users = all_users)