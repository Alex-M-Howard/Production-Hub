from flask import Blueprint, render_template, flash, redirect, url_for, session, g, jsonify, request, send_file

from models.nest import Nest, Machine

punch = Blueprint(
    'punch',
    __name__,
    static_folder='../../static',
    template_folder='../../templates/app',
    url_prefix='/punch'
    )


@punch.route("/")
def punch_home():
    return render_template("hubs/punch.html")

@punch.route("/data")
def get_punch_data():
    machine_id = Machine.query.filter_by(
        name='Murata', machine_type='Punch').one().id
    nests = Nest.query.filter_by(machine_id=machine_id).all()
    nests = Nest.many_to_json(nests)

    return nests

@punch.route("/sop")
def punch_sop():
    return render_template("sops/punch_sop.html")

