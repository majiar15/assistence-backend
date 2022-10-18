
from flask import Blueprint
from config.import_schema import  schedules_schema, Schedule
from config.import_schema import course_schema, courses_schema, Course
from config.Token import token_required, verificar_token

schedule=Blueprint('horario',__name__,url_prefix='/horario')

@schedule.route('/<teacherId>',methods=['GET'])
@token_required
def getScheduleTeacher(token,teacherId):
    print("El id del profesor es :",teacherId)
    courses = Course.query.filter_by(teacher_id=teacherId, active=True).all()

    print(courses_schema.dump(courses))
    aux=[]
    for course in courses:
      courseObj = course_schema.dump(course)
      shedules = Schedule.query.filter_by(course_id = courseObj['course_id'], active=True).all()
      aux.append({
         'course': courseObj,
         'schedule': schedules_schema.dump(shedules)
      })

    return aux

    
