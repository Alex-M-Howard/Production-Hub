from flask import Blueprint, render_template, flash, redirect, url_for, session, g, jsonify, request, send_file

from models.nest import Nest, Machine 

trumpf = Blueprint(
    'trumpf',
    __name__,
    static_folder='../../static',
    template_folder='../../templates/app',
    url_prefix='/trumpf'
    )


@trumpf.route("/")
def trumpf_home():
    return render_template("hubs/trumpf.html")

@trumpf.route("/data")
def get_trumpf_data():
    machine_id = Machine.query.filter_by(
        name='Trumpf', machine_type='Laser').one().id
    nests = Nest.query.filter_by(machine_id=machine_id).all()
    nests = Nest.many_to_json(nests)

    return nests

@trumpf.route("/trutops")
def trumpf_trutops():
    return render_template("sops/trutops.html")

@trumpf.route("/offline_loading")
def trumpf_offline_loading():
    return render_template("sops/offline_loading.html")
