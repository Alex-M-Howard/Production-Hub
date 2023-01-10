from flask import jsonify

from db import db


class Request(db.Model):
    """ 
    Request MODEL

    """

    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    to_change = db.Column(db.String)
    date = db.Column(db.Date, default=db.func.current_date())
    description = db.Column(db.String, nullable=False)
    requested_by = db.Column(db.String, nullable=False)
    request_type = db.Column(db.String, nullable=False)
    job_number = db.Column(db.String)
    date_completed = db.Column(db.Date, nullable=True)
    
    def __repr__(self): 
        return f"<Request #: {self.id}, What to change: {self.to_change}, Description: {self.description}, Requester: {self.requested_by}, Type: {self.request_type}>"
    
    @staticmethod
    def many_to_json(data):
        requests = []
        
        for request in data:
            requests.append({
                "id" : request.id,
                "to_change": request.to_change,
                "description": request.description,
                "requested_by" : request.requested_by,
                "request_type" : request.request_type,
                "job_number" : request.job_number,
                "date_completed" : request.date_completed.strftime("%m/%d/%Y") if request.date_completed else ""
            })
            
        return requests