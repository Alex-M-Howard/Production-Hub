from flask import jsonify

from db import db
from models.materials import Materials

class Nest(db.Model):
    """ 
    Nest MODEL

    """

    __tablename__ = 'nests'

    id = db.Column(db.Integer, primary_key=True)
    nest_name = db.Column(db.String, nullable=False)
    nested_with = db.Column(db.String, nullable=True)
    sheet_x = db.Column(db.Float, nullable=False)
    sheet_y = db.Column(db.Float, nullable=False)
    scrap = db.Column(db.Float, nullable=True)
    punch_forming = db.Column(db.Boolean, nullable=True)
    clamp_position_change = db.Column(db.Boolean, nullable=True)
    setup_time = db.Column(db.Float, nullable=True)
    process_time = db.Column(db.Float, nullable=True)
    date = db.Column(db.Date, nullable=True)
    
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    
    def __repr__(self):
        return f"<Nest #: {self.nest_name}, Material ID: {self.material_id}, Machine ID: {self.machine_id}, Date: {self.date}>"
    
    def many_to_json(data):
        nests = []
        
        for nest in data:
            if nest.date:
                nest.date = nest.date.isoformat()

            material = Materials.query.get(nest.material_id)
            
            nests.append({
                "id": nest.id,
                "nest_name": nest.nest_name,
                "nested_with": nest.nested_with,
                "sheet_x": nest.sheet_x,
                "sheet_y": nest.sheet_y,
                "scrap": nest.scrap,
                "punch_forming": nest.punch_forming,
                "clamp_position_change": nest.clamp_position_change,
                "setup_time": nest.setup_time,
                "process_time": nest.process_time,
                "date": nest.date,
                "material": material.material_name,
                "gauge": material.gauge,
            })
            
        return nests
        
   
class Machine(db.Model):
    """ Machine Model"""
    
    __tablename__ = 'machines'
    
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    machine_type = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f"<Machine Name: {self.name}, Type: {self.machine_type}>"
    
