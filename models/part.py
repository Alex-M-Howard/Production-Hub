from flask import jsonify

from db import db


class Part(db.Model):
    """ 
    Part MODEL

    """

    __tablename__ = 'parts'

    id = db.Column(db.Integer, primary_key=True)
    eco_number = db.Column(db.String, nullable=False)
    part_number = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    revision = db.Column(db.Integer, default=0)
    measuring_unit = db.Column(db.String, default="EA")
    item_type = db.Column(db.String)
    material_code = db.Column(db.String, default="M")
    replaces = db.Column(db.String)
    material_disposition = db.Column(db.String)
    effectivity_date = db.Column(db.String)
    continue_to_buy = db.Column(db.String)
    comments = db.Column(db.String)
    amada = db.Column(db.String, default='Incomplete')
    trumpf = db.Column(db.String, default='Incomplete')
    punch = db.Column(db.String, default='Incomplete')
    forming = db.Column(db.String, default='Incomplete')
    status = db.Column(db.String, default='Released')
    added = db.Column(db.Date, default=db.func.current_timestamp())
    

    def __repr__(self):
        return f"<Part #: {self.part_number}, Rev: {self.revision}, ECO#: {self.eco_number}>"

    @staticmethod
    def one_to_json(self):
        if self.effectivity_date:
            self.effectivity_date = self.effectivity_date.isoformat()

        return jsonify({
            "eco_number": self.eco_number,
            "part_number": self.part_number,
            "description": self.description,
            "revision": self.revision,
            "measuring_unit": self.measuring_unit,
            "item_type": self.item_type,
            "material_code": self.material_code,
            "replaces": self.replaces,
            "material_disposition": self.material_disposition,
            "effectivity_date": self.effectivity_date,
            "continue_to_buy": self.continue_to_buy,
            "comments": self.comments,
            "amada": self.amada,
            "trumpf": self.trumpf,
            "punch": self.punch,
            "forming": self.forming,
            "status": self.status
        })

    @staticmethod
    def many_to_json(data):
        eco_data = []

        for part in data:
            eco_data.append({
                "eco": part.eco_number,
                "part": part.part_number,
                "description": part.description,
                "revision": part.revision,
                "measuring_unit": part.measuring_unit,
                "item_type": part.item_type,
                "material_code": part.material_code,
                "replaces": part.replaces,
                "material_dis": part.material_disposition,
                "effectivity": part.effectivity_date,
                "continue_to_buy": part.continue_to_buy,
                "comments": part.comments,
                "amada": part.amada,
                "trumpf": part.trumpf,
                "punch": part.punch,
                "form": part.forming,
                "status": part.status,
                "date": part.added
            })

        return eco_data
