from flask import Blueprint, render_template, flash, redirect, url_for, session, g, jsonify, request, send_file
from db import db

from models.error import Error
from models.file import File
from models.forms import AddError, EditError

from datetime import datetime
from utilities import upload_file, list_all_objects_version, create_presigned_url

errors = Blueprint(
    'errors',
    __name__,
    static_folder='../../static',
    template_folder='../../templates/app',
    url_prefix='/errors'
    )


@errors.route("/")
def error_log():
    errors = Error.query.order_by(Error.date.desc()).all()
    
    for error in errors:
        error.date = error.date.strftime("%m/%d/%Y")
        
    return render_template("/error_log/error-log.html", errors=errors)    


@errors.route("/data")
def get_data():
    
    errors = Error.query.order_by(Error.date.desc()).all()
    errors = Error.many_to_json(errors)
    
    return errors


@errors.route("/add", methods=["GET", "POST"])
def add_to_errors():
    
    form = AddError()
    
    if form.validate_on_submit():
        
        new_error = Error(
            part_number = form.part_number.data,
            date = datetime.today().strftime("%m-%d-%Y"),
            machine = form.machine.data,
            description = form.description.data,
            root_cause = form.root_cause.data,
            notes = form.notes.data,
            name = form.name.data
        )
        
        db.session.add(new_error)
        db.session.commit()
        
        return redirect(url_for('errors.error_log'))
    
    return render_template("/error_log/add-error.html", form=form)


@errors.route("/edit/<error_id>", methods=["GET", "POST"])
def edit_error(error_id):
    
    error = Error.query.filter_by(id=error_id).one()
    
    form = EditError(obj=error)
    
    if form.validate_on_submit():
       
        error.part_number = form.part_number.data or error.part_number,
        error.machine = form.machine.data or error.machine,
        error.description = form.description.data or error.description,
        error.root_cause = form.root_cause.data or error.root_cause,
        error.notes = form.notes.data or error.notes,
        error.name = form.name.data or error.name
         
        db.session.commit()
        
        return redirect(url_for('errors.show_error', id=error_id))
    
    return render_template("/error_log/edit-error.html", form=form, error_id=error.id)


@errors.route("/<id>")
def show_error(id):
    
    error = Error.query.filter_by(id=id).one()
    files = File.query.filter_by(error_id=id).all()
    
    for file in files:
        # Create presigned URLS
        file.presigned_url = create_presigned_url(file.file_name, file.version)
        
    return render_template('/error_log/error.html', error=error, files=files)


@errors.route("/<id>/add", methods=["GET", "POST"])
def add_file(id):
    if request.method=="POST" :
        try:
            files = request.files.getlist('images')
            
            for file in files:
                upload_file(file=file, filename=file.filename)
                
                response = list_all_objects_version(file.filename)
                new_file = File(file_name=file.filename, error_id=id)
                
                try:
                    new_file.version = response["Versions"][0]["VersionId"]
                except:
                    new_file.version = '0'
                
                db.session.add(new_file)
                db.session.commit()

        except Exception as e:
            print(e)
            
        return redirect(url_for('errors.show_error', id=id))
    return render_template('/error_log/add-file.html', id=id)
