
from ast import dump
from flask import request, Blueprint
from config.Token import token_required, verificar_token

from config.database import db
from config.import_schema import Admin_schema, Admins_schema, Admin,course_student_schema, CourseStudent
from models.course import Course
from models.student import Student

from utils.has_str import has_str
from utils.response import  response


admin = Blueprint('admin',__name__, url_prefix='/api/admin') 

# protect routes
# @admin.before_request
# def verifyToken():
#     # try:
#     #     token = request.headers['Authorization'].split(' ')[1]
        
#     # except Exception as err:
#     #     return response(
#     #         403,
#     #         'Unauthorized',
#     #         data = err.__cause__
#     #     )

#     # return verificar_token()
#     return "hello"

@admin.route('/', methods=['POST'])
@token_required
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

    data = {'email': email, 'DNI': DNI, 'name': name}

    return response(
        201,
        'Admin create successfully',
        data= data ,
    )

@admin.route('/', methods=['GET'])
@token_required
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
    for item in resultAdmins:
        del item['password']
    return response(
        200,
        'get admin successfully',
        data= resultAdmins
    )
    
    
@admin.route('/<id>',methods=['GET'])
@token_required
def getOneAdmin(id):
    try:
        admin=Admin.query.filter_by(admin_id=id, active=True).first()
        res = Admin_schema.dump(admin)
        del res['password']
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
        data = res
    )

@admin.route('/<id>',methods=['PUT'])
@token_required
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
        'Admin Update successfully'
    )


@admin.route('/<id>',methods=['DELETE'])
@token_required
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
    


@admin.route('/enroll',methods=['POST'])
@token_required
def enrollStudent():

   
    request_data = request.get_json()

    courseId=None
    studentId=None
    if request_data:
        
        if "course_id" in request_data:
            
            if request_data['course_id']!='' and request_data['course_id']!=None:

                courseId=request_data['course_id']
                course=Course.query.get(courseId)
                if course==None:
                    return response(
                        404,
                        f"Course not found with id {courseId}",
                        
                    )

        if "student_id" in request_data:
            if request_data['student_id']!='' and request_data['student_id']!=None:
                studentId=request_data['student_id']
                student =Student.query.get(studentId)
                if student==None:
                    return response(
                        404,
                        f"Student not found with id {studentId}",
                        
                    )

        if studentId==None or courseId==None:
            return response(
                402,
                "Invalid parameters",
                data={
                    "course":courseId,
                    "student":studentId
                }
            )
        courseStudent=CourseStudent.query.filter_by(student_id=studentId, course_id=courseId).first()
        if courseStudent==None:

            auxcourseStudent=CourseStudent(studentId,courseId,True)
            db.session.add(auxcourseStudent)
            db.session.commit()
            return response(
                200,
                "Student successfully enrolled",
                data={
                    "enroll":True
                }
            )
        else:

            return response(
                200,
                'The student is already enrolled',
                data={
                    "enroll":True
                }
            )
        

