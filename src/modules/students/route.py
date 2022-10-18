
from typing import Any
from flask import request, jsonify, Blueprint
from utils.response import response
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

                return response(403,'Pamatros invalidos.',data)



            
            if not isEmail(email):
                return response(403,'Pamatro invalidos, el correo es invalido',{})

            new_student =Student(email,student_card,dni,name,True)
            db.session.add(new_student)
            db.session.commit()
           
            

        else:
            
            return response(403,'Parametros invalido, no envio ningun dato',)
    except Exception as err:
        db.session.rollback()
        return response(
            400,
            "error",
            data= err.__cause__
        )
    return response(
        200,
        "success",
        data=student_schema.dump(new_student)
    )
    



@student.route("/",methods=['GET'])
def getAllStudent():

    students=Student.query.filter_by(active=True).all()
    result=students_schema.dump(students)
    print("GET ALL STUDENT",result)

    return response(
        200,
        "success",
        data=result
    )

@student.route("/<id>",methods=['GET'])
def getOneStudent(id):
    student=Student.query.filter_by(DNI=id).first()
    return response(
        200,
        "success",
        data= student_schema.dump(student)
    )
 
   

@student.route("/<id>",methods=['PUT'])
def updateStudent(id):
    request_data = request.get_json()
    student=Student.query.filter_by(DNI=id).first()
    print(student)
    if student is None:
        return response(
            404,
            "Student not found",
            
        )
    if request_data:
        print(request_data)
        if "nombre" in request_data:

            if request_data['nombre']!='' and request_data['nombre']!=None:
                student.name = request_data['nombre']
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
    
        return response(
            200,
            "success",
            data= student_schema.dump(student)
        )
        #  student_schema.jsonify(student)
    
    else:
        return response(403,'No se enviaron ningun dato.',)


@student.route("/<id>",methods=['DELETE'])
def deleteStudent(id):

    student=Student.query.filter_by(DNI=id).first()
    student.active=False
    db.session.commit()
    return response(
            200,
            "Student deleted successfully",
            data= student_schema.dump(student)
        )
