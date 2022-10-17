
from config.database import db
from flask import jsonify, request, Blueprint
from config.import_schema import schedule_schema, schedules_schema, Schedule
from config.import_schema import course_schema, courses_schema, Course


schedule=Blueprint('horario',__name__,url_prefix='/horario')

@schedule.route('/<teacherId>',methods=['GET'])
def getScheduleTeacher(teacherId):
    print("El id del profesor es :",teacherId)
    result =(db.session.query(Course,Schedule).filter(Course.teacher_id==teacherId).filter(Schedule.course_id==Course.course_id).all())
    for course,schedule in result:
        print(course.name,' - ',schedule.day)
    return jsonify(result)

    
