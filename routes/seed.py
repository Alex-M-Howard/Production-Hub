from flask import Blueprint, render_template, flash, redirect, url_for, session, g, jsonify, request, send_file

from db import db

import csv

from models.materials import Blanks, Materials
from models.nest import Nest

DATA_PATH = 'C:/Users/ahoward/Desktop/scripts/data-explorer-flask/data/'

seed = Blueprint(
    'seed',
    __name__,
    static_folder='../../static',
    template_folder='../../templates/app',
    url_prefix='/seed'
)

@seed.route("/eco")
def seed_eco():
    return 'NOT AUTHORIZED'  # Needed only for seeding the database
    parts = []

    with open('C:/Users/ahoward/Desktop/aws/python/ECOdata.csv', 'r') as f:
        data = csv.reader(f)

        for line in data:

            if line[1] == '504024' or line[1] == 'Part #':
                continue

            try:
                part = Part(
                    eco_number=line[0],
                    part_number=line[1],
                    description=line[2],
                    revision=line[4],
                    measuring_unit=line[6],
                    item_type=line[7],
                    material_code=line[8],
                    replaces=line[9],
                    material_disposition=line[10],
                    effectivity_date=line[11],
                    continue_to_buy=line[12],
                    comments=line[13],
                    punch=line[14],
                    amada=line[15],
                    trumpf=line[16],
                    forming=line[17],
                    status=line[19],
                    added='12-15-2022'
                )

                parts.append(part)

            except Exception as e:
                print(e)
                with open('ECOerrors.txt', 'a') as error_file:
                    for each in line:
                        error_file.write(f'{each},')
                    error_file.write('\n')

    db.session.add_all(parts)
    db.session.commit()

    return 'SUCCESS'


@seed.route("/blanks")
def seed_blanks():
    """These are example blanks ONLY"""
    
    example_sizes = [
    (17, 96, 15, 5),
	(17, 96, 10, 3),
	(17, 96, 7, 2),
	(17, 96, 25, 9),
	(17, 96, 13, 2),
	(17, 96, 30, 1)
    ]
    
    blanks = []
    
    for each in example_sizes:
        new_blank = Blanks(
            material_id = each[0],
            length = each[1],
            width = each[2],
            quantity = each[3]
        )
    
        blanks.append(new_blank)
    
    db.session.add_all(blanks)
    db.session.commit()
    
    return 'SEEDED BLANKS'


@seed.route("/materials")
def seed_materials():

    materials = [
        ('VIT', 14),
        ('VIT', 18),
	    ('VIT', 20),
	    ('AZ', 14),
	    ('AZ', 16),
	    ('AZ', 18),
	    ('AZ', 20),
	    ('SS 301', 14),
	    ('SS 301', 16),
	    ('SS 301', 18),
	    ('SS 301', 20),
	    ('SS 301', 22),
   	    ('SS 304', 16),
   	    ('SS 304', 18),
	    ('SS 430', 20),
        ('SS 430', 22),
	    ('SS 301 2B', 14),
	    ('SS 301 2B', 18),
	    ('SS 430 2B', 18),
	    ('SS 430 2B', 20),
	    ('BRASS', 16),
	    ('MIRRORED BRASS', 16),
	    ('COPPER', 16),
	    ('MIRRORED COPPER', 16),
	    ('CRS', 11),
	    ('CRS', 13),
	    ('CRS', 16),
	    ('SS 316 2B', 16),
        ('AL', 16)
     ]

    to_add = []
    
    for each in materials:
        new_material = Materials(
            material_name = each[0],
            gauge = each[1]
        )
        
        to_add.append(new_material)
    
    db.session.add_all(to_add)
    db.session.commit()

    return 'SEEDED MATERIALS'


@seed.route("/nests")
def seed_nests():
    return 'NOT AUTHORIZED'

    Nest.__table__.drop(db.engine)
    Nest.__table__.create(db.engine)
    
    seed_amada()
    seed_trumpf()
    seed_punch()
    
    return 'SEEDED NESTS'


def seed_punch():
    nests = []

    with open(f"{DATA_PATH}/PunchData.txt", 'r') as f:
        data = csv.reader(f)

        for line in data:
            try:
                gauge = int(line[2])
                material_name = line[3]

                material_id = Materials.query.filter_by(
                    material_name=material_name, gauge=gauge).first().id

                if line[6].lower() == 'true':
                    line[6] = 1
                else:
                    line[6] = 0
                
                if line[7].lower() == 'true':
                    line[7] = 1
                else:
                    line[7] = 0
                
                
                new_nest = Nest(
                    machine_id=3,
                    nest_name=line[0],
                    nested_with=line[1],
                    material_id=material_id,
                    sheet_x=line[4],
                    sheet_y=line[5],
                    punch_forming=line[6],
                    clamp_position_change=line[7],
                    date=line[8]
                )

                nests.append(new_nest)

            except Exception as e:
                print(line, e)

    db.session.add_all(nests)
    db.session.commit()

    print("PUNCH NESTS SEEDED")
    return


def seed_trumpf():
    nests = []
    
    with open(f"{DATA_PATH}/TrumpfData.txt", 'r') as f:
        data = csv.reader(f)

        for line in data:
            try:
                gauge = int(line[1])
                material_name = line[3]

                material_id = Materials.query.filter_by(
                    material_name=material_name, gauge=gauge).first().id

                new_nest = Nest(
                    machine_id = 2,
                    nest_name = line[0],
                    nested_with = line[2],
                    material_id = material_id,
                    sheet_x = line[5],
                    sheet_y = line[4],
                    scrap = line[6],
                    date = line[7],
                    process_time = line[8]
                )
                
                nests.append(new_nest)
                
            except Exception as e:
                print(line, e)
    
    db.session.add_all(nests)
    db.session.commit()
    
    print("TRUMPF NESTS SEEDED")
    return    


def seed_amada():
    nests = []
    
    
    with open(f"{DATA_PATH}/AmadaData.txt", 'r') as f:
        data = csv.reader(f)
    
    
        for line in data:
            try:
                if line[1] == 'CR-13G':
                    line[1] = '13'
                    
                if line[1] == 'CRS-11G':
                    line[1] = '11'
                
                gauge = int(line[1])
                material_name = line[3]
                
                
                material_id = Materials.query.filter_by(material_name=material_name, gauge=gauge).first().id
                
                new_nest = Nest(
                    nest_name = line[0],
                    nested_with=line[2],
                    sheet_x=float(line[4]),
                    sheet_y=float(line[5]),
                    scrap=float(line[6]),
                    process_time = float(line[9]),
                    date = line[8],
                    machine_id = 1,
                    material_id = material_id
                )
                
                nests.append(new_nest)
            
            except Exception as e:
                print(line)
                print(e)
                
    db.session.add_all(nests)
    db.session.commit()
    
    print("AMADA NESTS SEEDED")
    return
