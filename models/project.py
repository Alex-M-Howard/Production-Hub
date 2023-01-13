from db import db
from datetime import datetime

class Project(db.Model):
    """ 
    Project MODEL

    """
    
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow())
    updated_by = db.Column(db.String)
    completed = db.Column(db.Date)
    user_name = db.Column(db.String, nullable=False)
    project_name = db.Column(db.String, nullable=False, unique=True)
    project_type = db.Column(db.String, nullable=False)
    product_line = db.Column(db.String)
    eco = db.Column(db.String)
    notes = db.Column(db.String)
    date_requested = db.Column(db.Date, nullable=False)
    progress = db.Column(db.Integer, default=0)
    late = db.Column(db.Boolean)
    status = db.Column(db.String, default='Incomplete')
    

    parts = db.relationship('ProtoPart', backref='project')

    
    def __repr__(self): return f"<Project #{self.id}: \nName - {self.project_name} \nOwner - {self.user_name} \nCreated - {self.created} \nUpdated: - {self.updated} \nCompleted - {self.completed}>"


class ProtoPart(db.Model):
    """
    Part MODEL

    """

    __tablename__ = 'proto_parts'
    
    id = db.Column(db.Integer, primary_key=True)
    part_number = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    updated_by = db.Column(db.String)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    material = db.Column(db.String)
    processes = db.Column(db.String)
    bin_location = db.Column(db.String)
    notes = db.Column(db.String)
    status = db.Column(db.String)
    punch = db.Column(db.Boolean, nullable=False, default=False)
    form = db.Column(db.Boolean, nullable=False, default=False)
    weld = db.Column(db.Boolean, nullable=False, default=False)
    polish = db.Column(db.Boolean, nullable=False, default=False)
    paint = db.Column(db.Boolean, nullable=False, default=False)
    assembly = db.Column(db.Boolean, nullable=False, default=False)
    enamel = db.Column(db.Boolean, nullable=False, default=False)
    fav = db.Column(db.Boolean, nullable=False, default=False)
    other = db.Column(db.Boolean, nullable=False, default=False)
    punch_status = db.Column(db.Boolean)
    form_status = db.Column(db.Boolean)
    weld_status = db.Column(db.Boolean)
    polish_status = db.Column(db.Boolean)
    paint_status = db.Column(db.Boolean)
    assembly_status = db.Column(db.Boolean)
    enamel_status = db.Column(db.Boolean)
    fav_status = db.Column(db.Boolean)
    other_status = db.Column(db.Boolean)
    
    files = db.relationship('ProtoFile', backref='part')

class ProtoFile(db.Model):
    """
    File MODEL

    """

    __tablename__ = 'proto_files'
    
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, nullable=False)
    version = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated_by = db.Column(db.String)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    part_id = db.Column(db.Integer, db.ForeignKey('proto_parts.id'))
    notes = db.Column(db.String)
    rev = db.Column(db.Integer, default=0)
    