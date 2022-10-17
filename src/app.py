
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from config.database import app
# from config.import_schema import Admin_schema, Admin, Admins_schema, teacher_schema, teachers_schema, Teacher, course_schema, courses_schema,Course, schedule_schema, schedules_schema,Schedule, classDb_schema, classDbs_schema, ClassDb, student_schema, students_schema, Student, course_student_schema, course_students_schema, CourseStudent, asisst_schema, asissts_schema, Asisst
# from modules.admin.routes import admin
from modules.admin.routes import admin
from flask_swagger_ui import get_swaggerui_blueprint

CORS(app)


### swagger specific ###
SWAGGER_URL = '/api/docs'
API_URL = 'http://localhost:5000/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(admin)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###
if __name__ == '__main__':
    app.run(debug=True)
 