from flask import Flask, render_template, g, session, redirect, url_for, json
from werkzeug.exceptions import HTTPException

import os

from config import set_config
from db import connect_to_db

from routes.amada import amada
from routes.punch import punch
from routes.trumpf import trumpf
from routes.forming import forming
from routes.requests import requests
from routes.general import general
from routes.errors import errors
from routes.seed import seed
from routes.user import user
from routes.documentation import docs
from routes.prototypes import proto
from routes.admin import admin


from models.user import User

# Create Flask app
app = Flask(__name__)

# Configure Setup
set_config(app)

# Connect to DB
connect_to_db(app)

# Give user object to g


@amada.before_request
@trumpf.before_request
@punch.before_request
@forming.before_request
@requests.before_request
@general.before_request
@errors.before_request
@seed.before_request
@docs.before_request
@proto.before_request
@user.before_request
@admin.before_request
@app.before_request
def add_user_globally():
    """If user is logged in, add user_id to Flask global"""

    if "current_user_id" in session:
        g.user = User.query.get(session["current_user_id"])

    else:
        g.user = None
        

# Custom error handlers


@amada.app_errorhandler(400)
@amada.app_errorhandler(401)
@amada.app_errorhandler(403)
@amada.app_errorhandler(404)
@amada.app_errorhandler(500)
@trumpf.app_errorhandler(400)
@trumpf.app_errorhandler(401)
@trumpf.app_errorhandler(403)
@trumpf.app_errorhandler(404)
@trumpf.app_errorhandler(500)
@punch.app_errorhandler(400)
@punch.app_errorhandler(401)
@punch.app_errorhandler(403)
@punch.app_errorhandler(404)
@punch.app_errorhandler(500)
@forming.app_errorhandler(400)
@forming.app_errorhandler(401)
@forming.app_errorhandler(403)
@forming.app_errorhandler(404)
@forming.app_errorhandler(500)
@requests.app_errorhandler(400)
@requests.app_errorhandler(401)
@requests.app_errorhandler(403)
@requests.app_errorhandler(404)
@requests.app_errorhandler(500)
@general.app_errorhandler(400)
@general.app_errorhandler(401)
@general.app_errorhandler(403)
@general.app_errorhandler(404)
@general.app_errorhandler(500)
@errors.app_errorhandler(400)
@errors.app_errorhandler(401)
@errors.app_errorhandler(403)
@errors.app_errorhandler(404)
@errors.app_errorhandler(500)
@seed.app_errorhandler(400)
@seed.app_errorhandler(401)
@seed.app_errorhandler(403)
@seed.app_errorhandler(404)
@seed.app_errorhandler(500)
@user.app_errorhandler(400)
@user.app_errorhandler(401)
@user.app_errorhandler(403)
@user.app_errorhandler(404)
@user.app_errorhandler(500)
@docs.app_errorhandler(400)
@docs.app_errorhandler(401)
@docs.app_errorhandler(403)
@docs.app_errorhandler(404)
@docs.app_errorhandler(500)
@admin.app_errorhandler(400)
@admin.app_errorhandler(401)
@admin.app_errorhandler(403)
@admin.app_errorhandler(404)
@admin.app_errorhandler(500)
@proto.app_errorhandler(400)
@proto.app_errorhandler(401)
@proto.app_errorhandler(403)
@proto.app_errorhandler(404)
@proto.app_errorhandler(500)
def handle_error(e):
    # Having user object show navbar if logged in
    if "current_user_id" in session:
        user = User.query.get(session["current_user_id"])
        g.user = user
    return render_template('error.html', error=e)


# Register routing blueprints
app.register_blueprint(amada)
app.register_blueprint(trumpf)
app.register_blueprint(punch)
app.register_blueprint(forming)
app.register_blueprint(requests)
app.register_blueprint(general)
app.register_blueprint(errors)
app.register_blueprint(seed)
app.register_blueprint(user)
app.register_blueprint(docs)
app.register_blueprint(proto)
app.register_blueprint(admin)



@app.route("/")
def home():
    return render_template('home.html')

@app.route("/production-project")
def dashboard():
    return render_template('dashboard.html')

@app.route("/todo")
def todo():
    return render_template('/projects/todo.html')

@app.route("/memory-game")
def memory_game():
    return render_template('/projects/memory.html')

@app.route("/frasier")
def frasier():
    return render_template('/projects/frasier/index.html')

@app.route("/resume")
def resume():
    return render_template('/resume.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("$PORT"))
