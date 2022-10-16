
from flask import Flask, request, jsonify

from config.database import app
from config.import_schema import Admin_schema, Admins_schema, teacher_schema, teachers_schema, course_schema, courses_schema, schedule_schema, schedules_schema, classDb_schema, classDbs_schema, student_schema, students_schema, course_student_schema, course_students_schema, asisst_schema, asissts_schema



@app.route('/', methods=['GET'])
def indexArticulo():
    print("loading admin...")
    all_articulos = Admin.query.all()
    resultArticulo = Admins_schema.dump(all_articulos)
    #return render_template("Articulos/index.html",  articulos =resultArticulo)
    return jsonify(resultArticulo) 

if __name__ == '__main__':
    app.run(debug=True)
 