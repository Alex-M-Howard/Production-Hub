from flask import Blueprint, render_template, flash, redirect, url_for, session, g, jsonify, request

from models.user import User
admin = Blueprint(
    'admin',
    __name__,
    static_folder='../../static',
    template_folder='../../templates/app',
    url_prefix='/admin'
)


@admin.route("/users")
def users():
    
    users = User.query.all()
    
    return render_template("admin/users.html", users=users)
