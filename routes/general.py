from flask import Blueprint, render_template, flash, redirect, url_for, session, g, jsonify, request
from sqlalchemy import select

from models.materials import Materials, Blanks
from models.part import Part
from models.forms import CreateIssueForm

from utilities import get_issues, post_issue

from db import db

general = Blueprint(
    'general',
    __name__,
    static_folder='../../static',
    template_folder='../../templates',
    url_prefix='/'
    )

@general.route("/nesting_calculator")
def nesting_calculator():
    return render_template("/misc/nesting-calculator.html")


@general.route("/blanks/inventory", methods=['GET', 'POST', 'DELETE'])
def blanks_inventory():
    if request.method == 'GET': # Get all blanks in inventory
        blanks = get_blanks_data()
        materials = get_materials_data()
        
        blank_material_names = set()
        [blank_material_names.add(blank['material_name']) for blank in blanks]    # Set comprehension to get unique material names
        
        material_names = set()
        [material_names.add(material['material_name']) for material in materials] # Set comprehension to get unique material names
        
        return render_template(
            "misc/blanks.html", 
            blanks=blanks, 
            materials=materials, 
            material_names=material_names, 
            blank_material_names=blank_material_names)

    if request.method == 'POST': # Add new blank to inventory
        data = request.get_json() 
        try:
            material_id = Materials.query.filter_by(
                material_name=data['material'], gauge=data['gauge']).first().id
        except Exception as e:
            print(e)
            return jsonify({'success': False, 'message': 'Material not found'})
        blanks = Blanks.query.filter_by(
            material_id=material_id, length=data['length'], width=data['width']).first()
        
        if blanks:
            blanks.quantity += int(data['quantity']) or 1
            db.session.commit()
        else:
            try:
                new_blank = Blanks(
                    material_id=material_id,
                    length=data['length'],
                    width=data['width'],
                    quantity=int(data['quantity']) or 1
                )
                db.session.add(new_blank)
                db.session.commit()
            except Exception as e:
                print(e)
                return jsonify({'success': False, 'message': 'Error adding blank'})
        
        return jsonify({'success': True})
    
    if request.method == 'DELETE': # Delete blank from inventory
        data = request.get_json()
        
        material_id = Materials.query.filter_by(
            material_name=data['material'], gauge=data['gauge']).first().id

        blanks = Blanks.query.filter_by(
            material_id=material_id, length=data['length'], width=data['width']).first()
        
        blanks.quantity -= 1
        
        if blanks.quantity:
            db.session.commit()
        else:
            db.session.delete(blanks)
            db.session.commit()
            return jsonify({'success': True, 'delete': True})
        
        return jsonify({'success': True, 'delete': False})


@general.route("/blanks/data")
def get_blanks_data():
    blanks = Blanks.query.order_by("material_id").all()
    blanks = Blanks.many_to_json(blanks)
    
    return blanks


@general.route("/materials/data")
def get_materials_data():
    materials = Materials.query.all()
    materials = Materials.many_to_json(materials)
    
    return materials


@general.route("/eco")
def eco_viewer():
    
    eco_data = get_eco_data()
    
    return render_template("/misc/eco.html", eco_data=eco_data)


@general.route("/eco/data")
def get_eco_data():
    parts = Part.query.order_by(Part.eco_number, Part.part_number.desc()).all()    
    parts = Part.many_to_json(parts)
    
    return parts


@general.route("/eco/data/obsolete")
def get_obsolete_eco_data():
    statement = select(Part.replaces).where(Part.replaces.is_not(None))
    parts = db.session.execute(statement)
    obsolete = []
    
    for each in parts.scalars():
        if '&' in each:
            splits = each.split(' & ')
            for split in splits:
                obsolete.append(split)
            continue    
        
        if len(each) > 12:
            each = each.split(' ')
            for split in each:
                obsolete.append(split)
            continue
        
        if 'F' in each:
            each = each.replace('F', '')
            
        obsolete.append(each)
    
    return obsolete


@general.route("/data_explorer")
def data_explorer():
    return render_template("/misc/explorer.html")


@general.route("/issues")
def issues():
    issues = get_issues()
    
    return render_template("/misc/issues.html", issues=issues)

@general.route("/issues/create", methods=['GET', 'POST'])
def create_issue():
    form = CreateIssueForm()
    
    if request.method == 'GET':
        return render_template("/misc/create-issue.html", form=form)
    
    if form.validate_on_submit():
        try:
            post_issue(form.data)
        except Exception as e:
            flash('Error creating issue. Try again.', 'danger')
            print(e)
            
    return redirect(url_for('general.issues'))

@general.route("/issues/data")
def all_issues():
    data = get_issues()
    issues = []
    
    for each in data:
        if each.pull_request:
            continue
        
        issues.append({
            "title": each.title, 
            "body": each.body, 
            "created_at": each.created_at.strftime("%m/%d/%y"),
            "updated_at": each.updated_at.strftime("%m/%d/%y") if each.updated_at else None,
            "comments": each.comments,
            "state": each.state,
            "closed_at": each.closed_at.strftime("%m/%d/%y") if each.closed_at else None,
            })
    
    return issues
