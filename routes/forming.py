from flask import Blueprint, render_template, flash, redirect, url_for, session, g, jsonify, request, send_file

from models.nest import Nest

forming = Blueprint(
    'forming',
    __name__,
    static_folder='../../static',
    template_folder='../../templates/app',
    url_prefix='/forming'
    )


@forming.route("/")
def forming_home():
    return render_template("hubs/forming.html")

@forming.route("/data")
def get_forming_data():
    nests = Nest.query.filter_by(nests.machine_id > 3).all()
    nests = Nest.many_to_json(nests)

    return nests

@forming.route("/salvagnini_guide")
def forming_salvagnini_guide():
    return render_template("sops/salvagnini_guide.html")

@forming.route("/bend_operation")
def forming_bend_operation():
    return render_template("sops/bend_operation.html")

@forming.route("/bend_parameters")
def forming_bend_params():
    return render_template("sops/bend_parameters.html")

@forming.route("/bend_users_guide")
def forming_bend_users():
    return render_template("sops/bend_users.html")

@forming.route("/data_explorer_sop")
def data_explorer():
    return render_template("sops/data_explorer.html")

@forming.route("/material_explorer_sop")
def material_explorer():
    return render_template("sops/material_explorer.html")

@forming.route("/parameter_explorer_sop")
def parameter_explorer():
    return render_template("sops/parameter_explorer.html")