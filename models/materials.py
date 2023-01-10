from db import db
from flask import jsonify

class Materials(db.Model):

    __tablename__ = 'materials'
    
    id = db.Column(db.Integer, primary_key=True)
    gauge = db.Column(db.Integer, nullable=False)
    material_name = db.Column(db.String, nullable=False)
    
    blanks = db.relationship('Blanks', back_populates='material')
    
    def __repr__(self):
        return f"<Material: ID: {self.id}, Gauge: {self.gauge}, Material Name: {self.material_name}"
    
    @staticmethod
    def many_to_json(data):
        materials = []

        for material in data:
            materials.append({
                "id": material.id,
                "material_name": material.material_name,
                "gauge": material.gauge
            })

        return materials
 
class Blanks(db.Model):
    
    __tablename__ = 'blanks'
    
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'))
    length = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    
    material = db.relationship('Materials', back_populates='blanks')   
    def __repr__(self):
        return f"<Blank: ID: {self.id}, Material Name: {self.material}, Length: {self.length}, Width: {self.width}, Quantity: {self.quantity}"
    
    @staticmethod
    def many_to_json(data):
        blanks = []

        for blank in data:
            blanks.append({
                "id" : blank.id,
                "material_name": blank.material.material_name,
                "gauge": blank.material.gauge,
                "length": blank.length,
                "width" : blank.width,
                "quantity" : blank.quantity
            })

        return blanks

class Sizes(db.Model):
    
    __tablename__ = 'sizes'
    
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'))
    length = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"<Size: Material ID: {self.material_id}, Length: {self.length}, Width: {self.width}"