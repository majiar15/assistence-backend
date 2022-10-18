
from typing import Any
from flask import request, jsonify, Blueprint
from utils.error import errorResponse
from utils.validate import isEmail
from config.import_schema import student_schema, students_schema, Student
from config.database import db


student=Blueprint('student',__name__,url_prefix='/estudiante')


@student.route('/',methods=['POST'])
def newStudent():
    try:
        request_data = request.get_json()
        
        email=None
        dni=None
        student_card=None
        name=None

        if request_data:
           
            if "email" in request_data:
                email=request_data['email'] 

            if "DNI" in request_data:
                dni=int(request_data['DNI'])

            if "carnet_estudiante" in request_data:
                student_card=int(request_data['carnet_estudiante']),

            if "nombre" in request_data:
                name=request_data['nombre']

            
            if email==None or dni==None or student_card==None or name==None:

                data={"email":email,"DNI":dni,"nombre":name,"carnet_estudiante":student_card}

                return jsonify(errorResponse(403,'Pamatros invalidos.',data)),403



            
            if not isEmail(email):
                return errorResponse(403,'Pamatro invalidos, el correo es invalido',{})

            new_student =Student(email,student_card,dni,name,True)
            db.session.add(new_student)
            db.session.commit()
           
            return student_schema.jsonify(new_student)

        else:
            
            return errorResponse(403,'Parametros invalido, no envio ningun dato',)
    except (RuntimeError, TypeError, NameError):
        return jsonify({
            "runtime":RuntimeError,
            "typeError":TypeError,
            "nameError":NameError
        })



@student.route("/",methods=['GET'])
def getAllStudent():

    students=Student.query.filter_by(active=True).all()
    result=students_schema.dump(students)
    print("GET ALL STUDENT",result)
    return jsonify(result),200

@student.route("/<id>",methods=['GET'])
def getOneStudent(id):
    student=Student.query.filter_by(DNI=id).first()
    return student_schema.jsonify(student)

@student.route("/<id>",methods=['PUT'])
def updateStudent(id):
    request_data = request.get_json()
    student=Student.query.filter_by(DNI=id).first()

    if request_data:
        print(request_data)
        if "nombre" in request_data:

            if request_data['nombre']!='' and request_data['nombre']!=None:
                student.name=request_data['nombre']
                print("El nuevo nombre es: ",request_data['nombre'])

        if "DNI" in request_data:
            if request_data['DNI']!='' and request_data['DNI']!=None:
                student.DNI=int(request_data['DNI'])
            
        if "email" in request_data:
            if request_data['email']!='' and request_data['email']!=None:

                email=request_data['email']

                if isEmail(email):
                    student.email=email
            
        if  "carnet_estudiante" in request_data:
            if request_data['carnet_estudiante']!='' and request_data['carnet_estudiante']!=None:

                student.student_card=int(request_data['carnet_estudiante'])
        
        db.session.commit()
    
        return student_schema.jsonify(student)
    
    else:
        return errorResponse(403,'No se enviaron ningun dato.',)


@student.route("/<id>",methods=['DELETE'])
def deleteStudent(id):

    student=Student.query.filter_by(DNI=id).first()
    student.active=False
    db.session.commit()
    return student_schema.jsonify(student)
