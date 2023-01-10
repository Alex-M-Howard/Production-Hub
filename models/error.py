from flask import jsonify

from db import db

class Error(db.Model):
    """ 
    Error MODEL

    """
    
    __tablename__ = 'errors'

    id = db.Column(db.Integer, primary_key=True)
    part_number = db.Column(db.String)
    date = db.Column(db.Date, nullable=False)
    machine = db.Column(db.String)
    description = db.Column(db.String, nullable=False)
    root_cause = db.Column(db.String)
    notes = db.Column(db.String)
    name = db.Column(db.String)
    
    def __repr__(self): 
        return f"<Error #: {self.id}, Date: {self.date}, Description: {self.description}>"

    @staticmethod
    def many_to_json(data):
        errors = []
        
        for error in data:
            errors.append({
                "id" : error.id,
                "part_number": error.part_number,
                "description": error.description,
                "date" : error.date,
                "machine" : error.machine,
                "root_cause" : error.root_cause,
                "notes" : error.notes,
                "name" : error.name
            })
            
        return errors
