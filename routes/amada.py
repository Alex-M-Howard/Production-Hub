from flask import Blueprint, render_template, flash, redirect, url_for, session, g, jsonify, request, send_file

from models.nest import Nest, Machine

amada = Blueprint(
    'amada',
    __name__,
    static_folder='../../static',
    template_folder='../../templates/app',
    url_prefix='/amada'
    )


@amada.route("/")
def amada_home():
    return render_template("hubs/amada.html")

@amada.route("/data")
def get_amada_data():
    machine_id = Machine.query.filter_by(name='Amada', machine_type='Laser').one().id
    nests = Nest.query.filter_by(machine_id=machine_id).all()
    nests = Nest.many_to_json(nests)
    
    return nests

@amada.route("/blankcam")
def amada_blankcam():
    return render_template("sops/blankcam.html")

@amada.route("/data_explorer_sop")
def data_explorer():
    return render_template("sops/data_explorer.html")

@amada.route("/material_explorer_sop")
def material_explorer():
    return render_template("sops/material_explorer.html")

@amada.route("/parameter_explorer_sop")
def parameter_explorer():
    return render_template("sops/parameter_explorer.html")
