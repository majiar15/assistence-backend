from flask import request, jsonify, Blueprint
# from jwt import encode
# from datetime import datetime
from hashlib import sha256

from config.database import db
from config.import_schema import Admins_schema, Admin

def has_str(srt):
    return sha256(srt.encode()).hexdigest() 

admin = Blueprint('admin',__name__, url_prefix='/admin') 

@admin.route('/', methods=['POST'])
def newAdmin():    
    email = request.json['email']
    DNI = request.json['DNI']
    name = request.json['name']
    password = has_str(request.json['password'])

    new_admin = Admin(email, DNI, name, password)
    db.session.add(new_admin)
    db.session.commit()

    return Admins_schema.jsonify(new_admin)

@admin.route('/', methods=['GET'])
def getAdmin():
    all_articulos = Admin.query.all()
    resultArticulo = Admins_schema.dump(all_articulos)
    #return render_template("Articulos/index.html",  articulos =resultArticulo)
    return jsonify(resultArticulo) 



    
