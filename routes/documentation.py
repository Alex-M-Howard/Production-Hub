from flask import Blueprint, render_template, flash, redirect, url_for, session, g, jsonify, request, send_file

docs = Blueprint(
    'docs',
    __name__,
    static_folder='../../static/documentation',
    template_folder='../../templates/documentation',
    url_prefix='/docs'
)

@docs.route("/")
def home():
    return render_template("/documentation/index.html")

@docs.route("/search")
def search():
    return render_template("/documentation/search.html")

@docs.route("/models")
def models():
    return render_template("/documentation/models/index.html")

@docs.route("/routes")
def routes():
    return render_template("/documentation/routes/index.html")
