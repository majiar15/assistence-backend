from flask import request, Blueprint
from config.Token import token_required

from config.database import db
from config.import_schema import teacher_schema, teachers_schema, Teacher

from utils.has_str import has_str
from utils.response import response


teacher = Blueprint('teacher',__name__, url_prefix='/teacher') 

@teacher.route('/', methods=['POST'])
@token_required
def newTeacher():    
    email = request.json['email']
    DNI = request.json['DNI']
    name = request.json['name']
    password = has_str(request.json['password'])

    new_teacher = Teacher(email, DNI, name, password, True)
    try:
        db.session.add(new_teacher)
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        return response(
            400,
            'Error creating teacher, please try again later',
            data=format(err.__cause__)
        )

    data = {'email': email, 'DNI': DNI, 'name': name}

    return response(
        201,
        'Teacher create successfully',
        data= data ,
    )

@teacher.route('/', methods=['GET'])
@token_required
def getTeacher():
    try:
        all_teachers = Teacher.query.filter_by(active=True).all()
        resultTeachers = teachers_schema.dump(all_teachers)
    except Exception as err:
        return response(
            400,
            'Error',
            data=format(err.__cause__)
        )
    for item in resultTeachers:
        del item['password']
    return response(
        200,
        'get teacher successfully',
        data= resultTeachers
    )
    
    
@teacher.route('/<id>',methods=['GET'])
@token_required
def getOneTeacher(id):
    try:
        teacher=Teacher.query.filter_by(teacher_id=id, active=True).first()
        resp = teacher_schema.dump(teacher)
        del resp['password']
    except Exception as err:
         return response(
            400,
            'Error',
            data=format(err.__cause__)
        )
    if teacher is None:
        return response(
            404,
            'Admin not found',
        )
    return response(
        200,
        'get Teacher successfully',
        data = resp
    )

   

@teacher.route('/<id>',methods=['PUT'])
@token_required
def updateTeacher(id):
    try:
        teacher=Teacher.query.filter_by(teacher_id=id, active=True).first()
        if teacher == None:
            return response(
                400,
                'Error',
                data=format(
                    'Teacher not found with id: {}'.format(id)
                )
            )
        request_data = request.get_json()
        
        if request_data:
            if "name" in request_data:
                if request_data['name']!='' and request_data['name']!=None:
                    teacher.name=request_data['name']
            if "email" in request_data:
                if request_data['email']!='' and request_data['email']!=None:
                    teacher.email=request_data['email']
                    
            if "password" in request_data:
                if request_data['password']!='' and request_data['password']!=None:
                    teacher.password= has_str(request_data['password'])

            if "DNI" in request_data:
                if request_data['DNI']!='' and request_data['DNI']!=None:
                    teacher.DNI=request_data['DNI']

            db.session.commit()
    except Exception as err:
        return response(
            400,
            'Error',
            data=format(err.__cause__)
        )            

    return response(
        200,
        "Teacher Update successfully"
    )


@teacher.route('/<id>',methods=['DELETE'])
@token_required
def deleteCourse(id):
    try:
        teacher=Teacher.query.get(id)
        teacher.active=False
        db.session.commit()
    except Exception as err:
        return response(
            400,
            'Error',
            data=format(err.__cause__)
        )
    return response(
        200,
        'Teacher Delete successfully',
        data= teacher_schema.dump(teacher)
    )
    


    
