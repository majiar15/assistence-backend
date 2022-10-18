
from config.database import db
from flask import jsonify, request, Blueprint
from config.import_schema import schedule_schema, schedules_schema, Schedule,Student
from config.import_schema import course_schema, courses_schema, Course,CourseStudent,ClassDb,classDb_schema,Asisst
from utils.response import  response
from datetime import date,datetime

assistance=Blueprint('assistance',__name__,url_prefix='/assistance')


@assistance.route('/',methods=['POST'])
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
                
                assist=Asisst.query.filter_by(student_id=studentId,classDb_id=claseBd.classDb_id)

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





