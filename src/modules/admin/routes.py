
from flask import request, Blueprint

from config.database import db
from config.import_schema import Admin_schema, Admins_schema, Admin

from utils.has_str import has_str
from utils.response import  response


admin = Blueprint('admin',__name__, url_prefix='/admin') 

@admin.route('/', methods=['POST'])
def newAdmin():    
    email = request.json['email']
    DNI = request.json['DNI']
    name = request.json['name']
    password = has_str(request.json['password'])

    new_admin = Admin(email, DNI, name, password, True)
    try:
        db.session.add(new_admin)
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        return response(
            400,
            'Error creating admin, please try again later',
            data=format(err.__cause__)
        )

    data = {'email': email, 'DNI': DNI, 'name': name, 'password': password}

    return response(
        201,
        'Admin create successfully',
        data= data ,
    )

@admin.route('/', methods=['GET'])
def getAdmin():
    try:
        all_admins = Admin.query.filter_by(active=True).all()
        resultAdmins = Admins_schema.dump(all_admins)
    except Exception as err:
        return response(
            400,
            'Error',
            data=format(err.__cause__)
        )
    return response(
        200,
        'get admin successfully',
        data= resultAdmins
    )
    
    
@admin.route('/<id>',methods=['GET'])
def getOneAdmin(id):
    try:
        admin=Admin.query.filter_by(admin_id=id, active=True).first()
        print(Admin_schema.jsonify(admin))
    except Exception as err:
         return response(
            400,
            'Error',
            data=format(err.__cause__)
        )
    if admin is None:
        return response(
            404,
            'Admin not found',
        )
    return response(
        200,
        'get Admin successfully',
        data = Admin_schema.dump(admin)
    )

@admin.route('/<id>',methods=['PUT'])
def updateAdmin(id):
    try:
        admin=Admin.query.filter_by(admin_id=id, active=True).first()
        if admin == None:
            return response(
                400,
                'Error',
                data=format(
                    'Admin not found with id: {}'.format(id)
                )
            )
        request_data = request.get_json()
        
        if request_data:
            if "name" in request_data:
                if request_data['name']!='' and request_data['name']!=None:
                    admin.name=request_data['name']
            if "email" in request_data:
                if request_data['email']!='' and request_data['email']!=None:
                    admin.email=request_data['email']
                    
            if "password" in request_data:
                if request_data['password']!='' and request_data['password']!=None:
                    admin.password= has_str(request_data['password'])

            if "DNI" in request_data:
                if request_data['DNI']!='' and request_data['DNI']!=None:
                    admin.DNI=request_data['DNI']

            db.session.commit()
    except Exception as err:
        return response(
            400,
            'Error',
            data=format(err.__cause__)
        )            

    return response(
        200,
        'Admin Update successfully',
        data = Admin_schema.dump(admin)
    )


@admin.route('/<id>',methods=['DELETE'])
def deleteAdmin(id):
    try:
        admin=Admin.query.get(id)
        admin.active=False
        db.session.commit()
    except Exception as err:
        return response(
            400,
            'Error',
            data=format(err.__cause__)
        )
    return response(
        200,
        'Admin Delete successfully',
        data= Admin_schema.dump(admin)
    )
    


    
