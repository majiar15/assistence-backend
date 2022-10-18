


from flask import jsonify, request, Blueprint
from config.import_schema import course_schema, courses_schema, Course
from config.import_schema import schedule_schema, schedules_schema,Schedule
from utils.response import response
from datetime import datetime
from config.database import db


course=Blueprint('course',__name__,url_prefix='/cursos')

@course.route('/',methods=['POST'])
def newCourse():

    try:
        request_data = request.get_json()
        teacherId=None
        name=None
        duration=None
        dateStart=None
        dateEnd=None
       
        if request_data:

            if "profesor_id" in request_data:
                auxTeacher=int(request_data['profesor_id'])
                if auxTeacher!=0 and auxTeacher!=None:
                    teacherId=auxTeacher
            
            if "nombre" in request_data:
                if request_data['nombre']!='' and request_data['nombre']!=None:
                    name=request_data['nombre']
            if "duracion" in request_data:
                if request_data['duracion']!='' and request_data['duracion']!=None:
                    duration=request_data['duracion']
                    # aux=    duration.strftime('%d/%m/%Y')
                    # return response(200,'Profesor registrado correctamente',{"duration":aux})
            if "fecha_inicial" in request_data:
                if request_data['fecha_inicial']!='' and request_data['fecha_inicial']!=None:
                    dateStart=datetime.strptime(request_data['fecha_inicial'],'%d/%m/%Y')
            
            if "fecha_fin" in request_data:
                if request_data['fecha_fin']!='' and request_data['fecha_fin']!=None:
                    dateEnd=datetime.strptime(request_data['fecha_fin'],'%d/%m/%Y')

            if teacherId==None or name==None or duration==None or dateStart==None or dateEnd ==None:

                data={"profesor_id":teacherId,"nombre":name,"duracion":duration,"fecha_inicial":dateStart,"fecha_fin":dateEnd}
                return response(403,'Verfique los datos ingresados, viene vacio',data)

            course=Course(teacherId,name,duration,dateStart,dateEnd,True)
            db.session.add(course)
            db.session.commit()
            if "horarios" in request_data:
                #respuesta de los horarios guardado en db solo falta responderle a usuario
                reps= newSchedule(course.course_id,list(request_data['horarios']))
            print('Respuesta de horarios',reps)
    
    except Exception as err:
        db.session.rollback()
        return response(
            400,
            'error',
            data= err.__cause__
        )    
    return response(
        200,
        'OK',
        data = {
            'course':course_schema.dump(course),
            'shedule': schedules_schema.dump(reps)
        }
    )

@course.route('/',methods=['GET'])
def getAllCourses():

    courses=Course.query.filter_by(active=True).all()
    return response(
            200,
            'get all course successfully',
            data = courses_schema.dump(courses)
        )
   

@course.route('/<id>',methods=['GET'])
def getOneCourse(id):

    course=Course.query.filter_by(course_id=id, active=True).first()
    schedule=Schedule.query.filter_by(course_id=id, active=True).all()
    return response(
        200,
        'OK',
        data = {
            'course': course_schema.dump(course),
            'shedule': schedules_schema.dump(schedule)
        }
    )
    course_schema.jsonify(course)

@course.route('/<id>',methods=['PUT'])
def updateCourse(id):
        try:
            course=Course.query.get(id)

            request_data = request.get_json()
            
            if request_data:
                if "profesor_id" in request_data:
                    auxTeacher=int(request_data['profesor_id'])
                    if auxTeacher!=0 and auxTeacher!=None:
                        course.teacher_id=auxTeacher
                
                if "nombre" in request_data:
                    if request_data['nombre']!='' and request_data['nombre']!=None:
                        course.name=request_data['nombre']
                if "duracion" in request_data:
                    if request_data['duracion']!='' and request_data['duracion']!=None:
                        course.duration=request_data['duracion']
                        # aux=    duration.strftime('%d/%m/%Y')
                        # return response(200,'Profesor registrado correctamente',{"duration":aux})
                if "fecha_inicial" in request_data:
                    if request_data['fecha_inicial']!='' and request_data['fecha_inicial']!=None:
                        course.date_start=datetime.strptime(request_data['fecha_inicial'],'%d/%m/%Y')
                
                if "fecha_fin" in request_data:
                    if request_data['fecha_fin']!='' and request_data['fecha_fin']!=None:
                        course.date_end=datetime.strptime(request_data['fecha_fin'],'%d/%m/%Y')
                
                db.session.commit()
                if "schedule" in request_data:
                    updateSchedule(request_data['schedule'])


        except Exception as err:
            db.session.rollback()
            return response(
                400,
                'error',
                data= err.__cause__
            )
        return response(
            200,
            'course update successfully',
            data = course_schema.jsonify(course)
        )
        

@course.route('/<id>',methods=['DELETE'])
def deleteCourse(id):
    course=Course.query.get(id)
    course.active=False
    db.session.commit()
    return response(
        200,
        'course delete successfully',
        data = course_schema.dump(course)
    )
     


def newSchedule(courseId,schedule):
    reps=[]
    for item in schedule:

        day=None
        timeStart=None
        timeEnd=None

        if "dia" in item:
            if item['dia']!='' and item['dia']!=None:
                day=item['dia']
        
        if "hora_inicio" in item:
            if item['hora_inicio']!='' and item['hora_inicio']!=None:
                timeStart=item['hora_inicio']

        if "hora_fin" in item:
            if item['hora_fin']!='' and item['hora_fin']!=None:
                timeEnd=item['hora_fin']
        auxSchedule=Schedule(courseId,day,timeStart,timeEnd, True)
        #print(schedule_schema.jsonify(auxSchedule))
        db.session.add(auxSchedule)
        db.session.commit()
        reps.append(auxSchedule)


    return reps



def updateSchedule(schedule):
    print(schedule)
    reps=[]
    for item in schedule:
        shedule=Schedule.query.get(item['id'])


        if "dia" in item:
            if item['dia']!='' and item['dia']!=None:
                shedule.day=item['dia']
        
        if "hora_inicio" in item:
            if item['hora_inicio']!='' and item['hora_inicio']!=None:
                shedule.time_start=item['hora_inicio']

        if "hora_fin" in item:
            if item['hora_fin']!='' and item['hora_fin']!=None:
                shedule.time_end=item['hora_fin']
        # auxSchedule=Schedule(courseId,day,timeStart,timeEnd, True)
        #print(schedule_schema.jsonify(auxSchedule))
        # db.session.add(auxSchedule)
        # db.session.commit()
        db.session.commit()
        reps.append(shedule)


    return reps



