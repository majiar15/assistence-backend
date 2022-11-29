
from flask import request, Blueprint
from config.Token import generar_token

from config.database import db
from config.import_schema import Admin_schema, Admins_schema, Admin, Teacher

from utils.has_str import has_str
from utils.response import  response


auth = Blueprint('auth',__name__, url_prefix='/api/auth') 

@auth.route('/login', methods=['POST'])
def login():    
    email = request.json['email']
    password = has_str(request.json['password'])
    try:
        admin=Admin.query.filter_by(email= email, active=True).first()

        if admin is None:
            teacher=Teacher.query.filter_by(email= email, active=True).first()
            if teacher is None:
                return {
                    "message": "Invalid Authentication!",
                    "data": None,
                    "error": "Unauthorized"
                }, 400
            if password != teacher.password:
                return response(
                    403,
                    'Invalid Login'
                )  
        else:
            if password != admin.password:
                return response(
                    403,
                    'Invalid Login'
                )
    except Exception as err:
         return response(
            400,
            'Error',
            data=format(err.__cause__)
        )
    
    if admin is None:
        token = generar_token(teacher.teacher_id)
    else:
        token = generar_token(admin.admin_id,True)

    return response(
        200,
        'Login successful',
        data = token['token']
    )

