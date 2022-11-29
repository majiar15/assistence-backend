
from ast import dump
from config.database import db
from flask import jsonify, request, Blueprint
from config.import_schema import students_schema, schedules_schema, Schedule,Student,asissts_schema
from config.import_schema import course_schema, classDbs_schema, Course,CourseStudent,ClassDb,classDb_schema,Asisst
from utils.response import  response
from datetime import date,datetime
from config.Token import token_required, verificar_token

assistance=Blueprint('assistance',__name__,url_prefix='/api/assistance')


@assistance.route('/',methods=['POST'])
@token_required
def newAssistance():

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
                        "course not found"
                    ) 

        if "student_id" in request_data:
            if request_data['student_id']!='' and request_data['student_id']!=None:
                studentId=request_data['student_id']

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
            return response(
                        404,
                        f"Student is not enrolled",  
                    )
        else:
            today=date.today()
            claseBd=ClassDb.query.filter_by(date=today,course_id=courseId).first()
            if claseBd==None:
                newclaseBd=ClassDb(courseId,today,True)
                db.session.add(newclaseBd),
                db.session.commit()

            

            today = date.weekday(date.today())
            result=Schedule.query.filter_by(course_id=courseId, day=str(today)).first()
            if result==None:
                return response(
                    404,
                    "there are no classes today"
                )
            currentTime=datetime.now().hour

            if int(result.time_start.split(':')[0])<=currentTime and currentTime<=int(result.time_end.split(':')[0]):
                
                assist=Asisst.query.filter_by(student_id=studentId,classDb_id=claseBd.classDb_id).first()
                
                if assist==None:

                    newAssist =Asisst(claseBd.classDb_id,studentId,True)
                    db.session.add(newAssist)
                    db.session.commit()
                    return response(
                        200,
                        "assistance taken correctly",
                        data={
                            "assistance":True
                        }
                    )
                else:
                    return response(
                        200,
                        "The student already has assistance",
                        data={
                            "assistance":True
                        }
                    )

            else:
                return response(
                    403,
                    "the class is not on schedule"
                )


    else:
        return response(402,"Invalid parameters",)


@assistance.route('/<fecha>/<courseId>',methods=['GET'])
@token_required
def getAssistDate(fecha,courseId):

    if fecha==None or courseId==None:
        return response(
            402,
            "Invalid parameters"
        )
    

  
    auxFecha=datetime.strptime(fecha,'%Y-%m-%d')
    print(auxFecha,courseId)
    classDbs=ClassDb.query.filter_by(course_id=int(courseId),date=fecha).first()

    

    auxStudent=[]
    if classDbs!=None:

        assistance=Asisst.query.filter_by(classDb_id=classDbs.classDb_id).all()

        
        if assistance!=None:

            for item in assistance:

                student=Student.query.get(int(item.student_id))

                
                if student!=None:
                    auxStudent.append(student)

            return response(
            200,
            "Ok",
            data=students_schema.dump(auxStudent)
            )
        else:

            return response(
            402,
            "Assist no found"
            )
    else:
         return response(
            402,
            "class not found"
            )  

        

