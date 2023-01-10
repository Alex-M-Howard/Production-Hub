from flask import Blueprint, render_template, flash, redirect, url_for, session, g, jsonify, request, send_file
from models.requests import Request
from models.forms import AddRequest
from db import db
from datetime import datetime
from utilities import email

COMPLETED_DATE_LIMIT = 5

requests = Blueprint(
    'requests',
    __name__,
    static_folder='../../static',
    template_folder='../../templates/app',
    url_prefix='/requests'
    )


@requests.route("/", methods=["GET", "POST", "DELETE"])
def requesting():
    form = AddRequest()
    today = datetime.now()
    
    if request.method == "GET": # Get all requests
        requests = Request.query.order_by(Request.date_completed.desc()).all()

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
        
        return render_template("misc/requests.html", form=form, requests=requests)

    if request.method == "POST": # Add new request
        data = request.get_json()
        
        new_request = Request(
            to_change=data['to_change'],
            description=data['description'],
            requested_by=data['requested_by'],
            request_type=data['request_type'],
            job_number=data.get('job_number'))

        db.session.add(new_request)
        db.session.commit()
        
        email(data) # Send email to programming team
        
        return jsonify({'success': True, 'message': 'Request added'})
    
    if request.method == "DELETE": # Stage request for deletion
        data = request.get_json()
        
        req = Request.query.get(data['id'])
        req.date_completed = today
        req.job_number = data.get('job_number')
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Request staged for deletion'})
