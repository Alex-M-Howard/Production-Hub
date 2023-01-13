from flask import Blueprint, render_template, flash, redirect, url_for, session, g, request, jsonify
import flask
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from routes.requests import COMPLETED_DATE_LIMIT

from models.forms import ProjectForm, EditProjectForm, PartForm, EditPartForm, AddFileForm
from models.project import Project, ProtoPart, ProtoFile
from models.materials import Materials
from models.requests import Request

from db import db

from utilities import *

proto = Blueprint(
    'proto',
    __name__,
    static_folder='../../static',
    template_folder='../../templates/prototypes',
    url_prefix='/proto'
)


@proto.route('/')
def home():
    try:
        projects = Project.query.filter_by(status='Incomplete').all()
        date = datetime.now().date()

        for project in projects:
            if project.date_requested < date:
                project.late = True
    except Exception as e:
        print(e)
        projects = False
        
    requests = Request.query.order_by(Request.date_completed.desc()).all()
    today = datetime.now()
    
    for req in requests:
        try:
            # Delete requests that have been completed for 5 days
            if (today - datetime.combine(
                    req.date_completed, datetime.min.time())).days >= COMPLETED_DATE_LIMIT:
                db.session.delete(req)
                db.session.commit()
        except Exception as e:
            print(e)
            pass

    return render_template('/home.html', projects=projects, requests=requests)


@proto.route('/all_projects')
def show_projects():
    projects = Project.query.all()

    for project in projects:
        product_line = project.product_line
        product_line = product_line.replace("{", "")
        product_line = product_line.replace("}", "")
        product_line = product_line.replace(",", ", ")
        project.product_line = product_line
        
        if project.updated == None:
            project.updated = ""

    return render_template('/prototypes/projects.html', projects=projects)


@proto.route('/createProject', methods=["GET", "POST"])
def create_project():
    form = ProjectForm()

    if form.validate_on_submit():
        project = Project.query.filter_by(project_name=form.project_name.data).first()
        
        if project:
            flash("Project already exists. Please select a new name.", "danger")
            return redirect(url_for('proto.create_project'))
        

        try:
            timestamp = datetime.now().isoformat().split('.')[0]

            new_project = Project(
                user_name=g.user.name(),
                project_name=form.project_name.data,
                project_type=form.project_type.data,
                product_line=form.product_line.data,
                eco=form.eco.data,
                notes=form.notes.data,
                date_requested=form.date_requested.data,
                created=timestamp,
                updated_by=g.user.name()
            )

            db.session.add(new_project)
            db.session.commit()

        except Exception as e:
            print(e)
            return redirect(url_for('proto.show_projects'))
        
        return redirect(url_for('proto.show_project', project_name=form.project_name.data))
                        
    return render_template('/prototypes/create_project.html', form=form)


@proto.route('/<project_name>', methods=["GET"])
def show_project(project_name):
    project = Project.query.filter_by(project_name=project_name).one()
    parts = ProtoPart.query.filter_by(project_id=project.id).all()
    
    product_line = project.product_line
    product_line = product_line.replace("{", "")
    product_line = product_line.replace("}", "")
    product_line = product_line.replace(",", ", ")
    project.product_line = product_line
    
    for each in parts:
        each.total_processes = count_part_processes(each)
        each.total_processes_completed = count_part_processes_completed(each)
        

    return render_template('/prototypes/project.html', project=project, parts=parts)


@proto.route('/<project_name>/edit', methods=["GET", "POST"])
def edit_project(project_name):

    if "current_user_id" not in session:
        flash("You must be logged in to edit a project", "danger")
        return redirect(url_for('user.login_page'))

    project = Project.query.filter_by(project_name=project_name).one()

    form = EditProjectForm(obj=project)

    if form.validate_on_submit():
        try:
            project.project_name = form.project_name.data or project.project_name
            project.project_type = form.project_type.data or project.project_type
            project.product_line = form.product_line.data or project.product_line
            project.eco = form.eco.data
            project.notes = form.notes.data
            project.date_requested = form.date_requested.data
            project.updated_by = g.user.name()
            project.progress = form.progress.data

            timestamp = datetime.now().isoformat().split('.')[0]
            project.updated = timestamp
            
            if project.progress == 100:
                project.completed = timestamp
                project.status = "Completed"
            else:
                project.completed = None
                project.status = "Incomplete"

            db.session.commit()

        except Exception as e:
            print(e)

        return redirect(url_for('proto.show_project', project_name=project.project_name))

    return render_template('/prototypes/edit_project.html', form=form, project=project)


@proto.route("/get_all_projects_incomplete")
def get_all_projects_incomplete():
    projects = []
    all_projects = Project.query.filter_by(status='Incomplete')

    for each in all_projects:
        
        product_line = each.product_line
        product_line = product_line.replace("{", "")
        product_line = product_line.replace("}", "")
        product_line = product_line.replace(",", ", ")
        each.product_line = product_line
        
        each.date_requested = each.date_requested.strftime("%m-%d-%Y")
        try:
            each.created = each.created.strftime("%m-%d-%Y")
        except:
            pass
        try:
            each.updated = each.updated.strftime("%m-%d-%Y")
        except:
            pass

        projects.append({
            "project_name": each.project_name,
            "user_name": each.user_name,
            "project_type": each.project_type or " ",
            "product_line": each.product_line or " ",
            "eco": each.eco or " ",
            "notes": each.notes or " ",
            "date_requested": each.date_requested,
            "progress": each.progress,
            "created": each.created,
            "updated": each.updated or " ",
            "updated_by": each.updated_by
        })

    return projects


@proto.route("/get_all_projects_complete")
def get_all_projects_complete():
    projects = []
    all_projects = Project.query.filter_by(status='Completed')

    for each in all_projects:
        product_line = each.product_line
        product_line = product_line.replace("{", "")
        product_line = product_line.replace("}", "")
        product_line = product_line.replace(",", ", ")
        each.product_line = product_line
        
        each.date_requested = each.date_requested.strftime("%m-%d-%Y")
        try:
            each.created = each.created.strftime("%m-%d-%Y")
        except:
            pass
        try:
            each.updated = each.updated.strftime("%m-%d-%Y")
        except:
            pass
        try:
            each.completed = each.completed.strftime("%m-%d-%Y")
        except:
            pass

        projects.append({
            "project_name": each.project_name,
            "user_name": each.user_name,
            "project_type": each.project_type or " ",
            "product_line": each.product_line or " ",
            "eco": each.eco or " ",
            "notes": each.notes or " ",
            "date_requested": each.date_requested,
            "progress": each.progress,
            "completed": each.completed,
            "created": each.created,
            "updated": each.updated or " ",
        })

    return projects


@proto.route("/get_my_projects_incomplete")
def get_my_projects_incomplete():
    projects = []
    my_projects = Project.query.filter_by(
        user_name=g.user.name(), status='Incomplete')

    for each in my_projects:
        product_line = each.product_line
        product_line = product_line.replace("{", "")
        product_line = product_line.replace("}", "")
        product_line = product_line.replace(",", ", ")
        each.product_line = product_line
        
        each.date_requested = each.date_requested.strftime("%m-%d-%Y")
        try:
            each.created = each.created.strftime("%m-%d-%Y")
        except:
            pass
        try:
            each.updated = each.updated.strftime("%m-%d-%Y")
        except:
            pass

        projects.append({
            "project_name": each.project_name,
            "user_name": each.user_name,
            "project_type": each.project_type or " ",
            "product_line": each.product_line or " ",
            "eco": each.eco or " ",
            "notes": each.notes or " ",
            "date_requested": each.date_requested,
            "progress": each.progress,
            "created": each.created,
            "updated": each.updated or " ",
            "updated_by": each.updated_by
        })

    return projects


@proto.route("/get_my_projects_complete")
def get_my_projects_complete():
    projects = []
    my_projects = Project.query.filter_by(
        user_name=g.user.name(), status='Completed')
    
    for each in my_projects:
        product_line = each.product_line
        product_line = product_line.replace("{", "")
        product_line = product_line.replace("}", "")
        product_line = product_line.replace(",", ", ")
        each.product_line = product_line
    
        each.date_requested = each.date_requested.strftime("%m-%d-%Y")
        try:
            each.created = each.created.strftime("%m-%d-%Y")
        except:
            pass
        try:
            each.updated = each.updated.strftime("%m-%d-%Y")
        except:
            pass
        try:
            each.completed = each.completed.strftime("%m-%d-%Y")
        except:
            pass

        projects.append({
            "project_name": each.project_name,
            "user_name": each.user_name,
            "project_type": each.project_type or " ",
            "product_line": each.product_line or " ",
            "eco": each.eco or " ",
            "notes": each.notes or " ",
            "date_requested": each.date_requested,
            "progress": each.progress,
            "completed": each.completed,
            "created": each.created,
            "updated": each.updated or " ",
        })

    return projects


@proto.route("/<project_name>/create_part", methods=["GET", "POST"])
def create_part(project_name):
    project = Project.query.filter_by(project_name=project_name).one()
    
    if flask.request.method == "GET":
        material_choices = set([m.material_name for m in set(Materials.query.all())])

        return render_template("/prototypes/create_part.html", project_name=project_name, materials=material_choices)

    if flask.request.method == "POST":
        try:
            part_check = ProtoPart.query.filter_by(part_number=flask.request.form.get('part_number'), project_id=project.id).first()
            if(part_check):
                flash('Part Number already exists in this project!', 'danger')
                return redirect(url_for('proto.create_part', project_name=project_name))
            
            new_part = ProtoPart(
                part_number=flask.request.form.get('part_number'),
                description=flask.request.form.get('description'),
                project_id=project.id,
                material=flask.request.form.get('material'),
                bin_location=flask.request.form.get('bin_location'),
                notes=flask.request.form.get('notes'),
                status=flask.request.form.get('status'),
                updated_by=g.user.name(),
                punch=flask.request.form.get('punch'),
                form=flask.request.form.get('form'),
                weld=flask.request.form.get('weld'),
                polish=flask.request.form.get('polish'),
                paint=flask.request.form.get('paint'),
                assembly=flask.request.form.get('assembly'),
                enamel=flask.request.form.get('enamel'),
                fav=flask.request.form.get('fav'),
                other=flask.request.form.get('other')
            )
            
            new_part.punch = True if new_part.punch == 'on' else False
            new_part.form = True if new_part.form == 'on' else False
            new_part.weld = True if new_part.weld == 'on' else False
            new_part.polish = True if new_part.polish == 'on' else False
            new_part.paint = True if new_part.paint == 'on' else False
            new_part.assembly = True if new_part.assembly == 'on' else False
            new_part.enamel = True if new_part.enamel == 'on' else False
            new_part.fav = True if new_part.fav == 'on' else False
            new_part.other = True if new_part.other == 'on' else False
            
            project.updated_by = g.user.name()
            timestamp = datetime.now().isoformat().split('.')[0]
            project.updated = timestamp

            db.session.add(new_part)
            db.session.commit()

            set_project_completion(project.id)
            
        except Exception as e:
            print(e)

        return redirect(url_for('proto.show_part', project_name=project_name, part_number=new_part.part_number))


@proto.route("/<project_name>/<part_number>")
def show_part(project_name, part_number):
    project = Project.query.filter_by(project_name=project_name).one()
    part = ProtoPart.query.filter_by(part_number=part_number, project_id=project.id).one()
    files = ProtoFile.query.filter_by(part_id=part.id, project_id=project.id).all()
    
    files_set = set()

    for each in files:
        files_set.add(each.file_name)
        
    files = []
    
    for each in files_set:
        file = ProtoFile.query.filter_by(file_name=each, part_id=part.id, project_id=project.id).order_by(ProtoFile.created.desc()).first()
        file.presigned_url = create_presigned_url(file.file_name, version_id=file.version)
        
        files.append(file)

    
    part.proccesses = []
    if part.punch: part.proccesses.append({"name": 'Punch', "status": part.punch_status})
    if part.form: part.proccesses.append({"name": 'Form', "status": part.form_status})
    if part.weld: part.proccesses.append({"name": 'Weld', "status": part.weld_status})
    if part.polish: part.proccesses.append({"name": 'Polish', "status": part.polish_status})
    if part.paint: part.proccesses.append({"name": 'Paint', "status": part.paint_status})
    if part.assembly: part.proccesses.append({"name": 'Assembly', "status": part.assembly_status})
    if part.enamel: part.proccesses.append({"name": 'Enamel', "status": part.enamel_status})
    if part.fav: part.proccesses.append({"name": 'Fav', "status": part.fav_status})
    if part.other: part.proccesses.append({"name": 'Other', "status": part.other_status})
    
    return render_template('/prototypes/part.html', project_name=project_name, part=part, files=files)


@proto.route("/<project_name>/<part_number>/edit", methods=["GET", "POST"])
def edit_part(project_name, part_number):
    project = Project.query.filter_by(project_name=project_name).one()
    part = ProtoPart.query.filter_by(part_number=part_number, project_id=project.id).one()

    if flask.request.method == "GET":
        material_choices = [m.material_name for m in set(Materials.query.all())]
        return render_template('/prototypes/edit_part.html', project_name=project_name, part=part, materials=set(material_choices))


    if flask.request.method == "POST":
        try:
            part.part_number = flask.request.form.get('part_number') or part.part_number
            part.description = flask.request.form.get('description')
            part.material = flask.request.form.get('material')
            part.bin_location = flask.request.form.get('bin_location')
            part.notes = flask.request.form.get('notes')
            part.status = flask.request.form.get('status')
            part.punch = flask.request.form.get('punch')
            part.form = flask.request.form.get('form')
            part.weld = flask.request.form.get('weld')
            part.polish = flask.request.form.get('polish')
            part.paint = flask.request.form.get('paint')
            part.assembly = flask.request.form.get('assembly')
            part.enamel = flask.request.form.get('enamel')
            part.fav = flask.request.form.get('fav')
            part.other = flask.request.form.get('other')
            
            part.updated_by = g.user.name()
            project.updated_by = g.user.name()
            timestamp = datetime.now().isoformat().split('.')[0]
            project.updated = timestamp
            
            part.punch = True if part.punch == 'on' else False
            part.form = True if part.form == 'on' else False
            part.weld = True if part.weld == 'on' else False
            part.polish = True if part.polish == 'on' else False
            part.paint = True if part.paint == 'on' else False
            part.assembly = True if part.assembly == 'on' else False
            part.enamel = True if part.enamel == 'on' else False
            part.fav = True if part.fav == 'on' else False
            part.other = True if part.other == 'on' else False

            db.session.commit()
            
            set_project_completion(project.id)

        except Exception as e:
            print(e)

        return redirect(url_for('proto.show_part', part_number=part_number, project_name=project_name))


@proto.route("/<project_name>/<part_number>/add_file", methods=["GET", "POST"])
def add_file(project_name, part_number):

    form = AddFileForm()

    if form.validate_on_submit():
        try:       
            submitted_files = form.file.data

            project = Project.query.filter_by(project_name=project_name).one()
            part = ProtoPart.query.filter_by(part_number=part_number).one()
            
            for file in submitted_files:                
                files = ProtoFile.query.filter_by(file_name=file.filename).order_by(ProtoFile.rev.desc()).all()
                
                latest_rev = files[0].rev if files else -1
                
                upload_file(
                    file=file, 
                    filename=file.filename, 
                    project_id=project.id, 
                    part_id=part.id, 
                    uploaded_by=g.user.name(),
                    notes=form.notes.data)
                
                timestamp = datetime.now()
                project.updated = timestamp
                project.updated_by = g.user.name()
                part.updated_by = g.user.name()
                
                obj = get_obj(file.filename)
              
                new_file = ProtoFile(
                    file_name=file.filename,
                    project_id=project.id,
                    part_id=part.id,
                    version=obj["VersionId"],
                    notes = form.notes.data,
                    updated_by=g.user.name(),
                    rev = latest_rev + 1
                )

                db.session.add(new_file)
                
            db.session.commit()

        except Exception as e:
            flash('Error uploading file', 'danger')
            print(e)
            return redirect(url_for('proto.add_file', project_name=project_name, part_number=part_number))

        return redirect(url_for('proto.show_part', project_name=project_name, part_number=part_number))

    return render_template('/prototypes/add-file.html', form=form, project_name=project_name, part_number=part_number)


@proto.route("/<project_name>/<part_number>/<file_name>/versions")
def show_versions(project_name, part_number, file_name):
    
    versions = ProtoFile.query.filter_by(file_name=file_name).all()
    print(versions)
    for file in versions:
        date = file.created.strftime("%m/%d/%Y %H:%M:%S")

        file.presigned_url = create_presigned_url(file_name, version_id=file.version)
        file.created = date
    
    return render_template("/prototypes/file-versions.html", files=versions, part_number=part_number, project_name=project_name, file_name=file_name)


@proto.route('/<project_name>/<part_number>/<file_name>/versions/<version_id>', methods=["POST"])
def delete_file(project_name, part_number, file_name, version_id):
    try:
        delete_s3_object(file_name, version_id=version_id)
        project = Project.query.filter_by(project_name=project_name).one()
        part = ProtoPart.query.filter_by(part_number=part_number).one()
        timestamp = datetime.now().isoformat().split('.')[0]
        project.updated = timestamp
        project.updated_by = g.user.name()
        part.updated_by = g.user.name()
        
        file = ProtoFile.query.filter_by(file_name=file_name, version=version_id).one()
        db.session.delete(file)
        db.session.commit()
    except Exception as e:
        print(e)
        flash(f'Error deleting file: {file_name}', 'danger')
        return redirect(url_for('proto.show_part', project_name=project_name, part_number=part_number))

    flash(f'Success deleting file: {file_name}', 'success')
    return redirect(url_for('proto.show_part', project_name=project_name, part_number=part_number))


@proto.route("/my_projects")
def show_my_projects():
    projects = Project.query.filter_by(user_name=g.user.name()).all()

    for project in projects:
        product_line = project.product_line
        product_line = product_line.replace("{", "")
        product_line = product_line.replace("}", "")
        product_line = product_line.replace(",", ", ")
        project.product_line = product_line
        
        if project.updated == None:
            project.updated = ""

    return render_template('/prototypes/my-projects.html', projects=projects)


@proto.route("/update_process", methods=["POST"])
def update_process():
    if flask.request.method == "POST":
        
        data = flask.request.get_json()
        
        try:
            project = Project.query.filter_by(project_name=data['projectName']).one()
            part = ProtoPart.query.filter_by(part_number=data['partName'], project_id=project.id).one()

            if data['process'] == 'punch': part.punch_status = data['status']
            if data['process'] == 'form': part.form_status = data['status']
            if data['process'] == 'weld': part.weld_status = data['status']
            if data['process'] == 'polish': part.polish_status = data['status']
            if data['process'] == 'paint': part.paint_status = data['status']
            if data['process'] == 'assembly': part.assembly_status = data['status']
            if data['process'] == 'enamel': part.enamel_status = data['status']
            if data['process'] == 'fav': part.fav_status = data['status']
            if data['process'] == 'other': part.other_status = data['status']

            
            

            db.session.commit()
            
            set_project_completion(project.id)
                
        except Exception as e:
            print(e)
            return "Failure"
        
        return "success"


def count_project_processes(project_id):
    project = Project.query.filter_by(id=project_id).one()
    parts = ProtoPart.query.filter_by(project_id=project.id).all()
    
    total_processes = 0
    
    for each in parts:
        
        if each.punch: total_processes += 1
        if each.form: total_processes += 1
        if each.weld: total_processes += 1
        if each.polish: total_processes += 1
        if each.paint: total_processes += 1
        if each.assembly: total_processes += 1
        if each.enamel: total_processes += 1
        if each.fav: total_processes += 1
        if each.other: total_processes += 1
    
    return total_processes


def count_project_processes_done(project_id):
    project = Project.query.filter_by(id=project_id).one()
    parts = ProtoPart.query.filter_by(project_id=project.id).all()
    
    finished_processes = 0
    
    for each in parts:
        
        if not each.punch:each.punch_status = None
        if not each.form: each.form_status = None
        if not each.weld:each.weld_status = None
        if not each.polish:each.polish_status = None
        if not each.paint:each.paint_status = None
        if not each.assembly:each.assembly_status = None
        if not each.enamel:each.enamel_status = None
        if not each.fav:each.fav_status = None
        if not each.other:each.other_status = None
        
        if each.punch_status == True: finished_processes += 1
        if each.form_status == True: finished_processes += 1
        if each.weld_status == True: finished_processes += 1
        if each.polish_status == True: finished_processes += 1
        if each.paint_status == True: finished_processes += 1
        if each.assembly_status == True: finished_processes += 1
        if each.enamel_status == True: finished_processes += 1
        if each.fav_status == True: finished_processes += 1
        if each.other_status == True: finished_processes += 1
    
    return finished_processes


def set_project_completion(project_id):
    project = Project.query.filter_by(id=project_id).one()
    total_processes = count_project_processes(project_id)
    finished_processes = count_project_processes_done(project_id)
    
    project.progress = round((finished_processes / total_processes) * 100, 2)
    
    timestamp = datetime.now().isoformat().split('.')[0]
    
    if project.progress == 100:
        project.completed = timestamp
        project.status = "Completed"
    else:
        project.completed = None
        project.status = "Incomplete"
    
    db.session.commit()


def count_part_processes(part):
    total_processes = 0
    
    if part.punch: total_processes += 1
    if part.form: total_processes += 1
    if part.weld: total_processes += 1
    if part.polish: total_processes += 1
    if part.paint: total_processes += 1
    if part.assembly: total_processes += 1
    if part.enamel: total_processes += 1
    if part.fav: total_processes += 1
    if part.other: total_processes += 1
    
    return total_processes
    

def count_part_processes_completed(part):
    total_complete = 0
    
    if not part.punch:part.punch_status = None
    if not part.form: part.form_status = None
    if not part.weld:part.weld_status = None
    if not part.polish:part.polish_status = None
    if not part.paint:part.paint_status = None
    if not part.assembly:part.assembly_status = None
    if not part.enamel:part.enamel_status = None
    if not part.fav:part.fav_status = None
    if not part.other:part.other_status = None
    
    if part.punch_status: total_complete += 1
    if part.form_status: total_complete += 1
    if part.weld_status: total_complete += 1
    if part.polish_status: total_complete += 1
    if part.paint_status: total_complete += 1
    if part.assembly_status: total_complete += 1
    if part.enamel_status: total_complete += 1
    if part.fav_status: total_complete += 1
    if part.other_status: total_complete += 1
    
    return total_complete
