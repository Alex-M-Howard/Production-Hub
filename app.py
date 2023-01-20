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


@app.errorhandler(HTTPException)
@app.errorhandler(Exception)
def handle_error(e):
    if e.code == None:
        e.code == 500
    
    if e.description == None:
        e.description = "Something went wrong. Please try again later."
        
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
    return redirect(url_for('proto.home'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("$PORT"))
