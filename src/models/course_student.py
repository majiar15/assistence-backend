
from config.database import db, ma, app

class CourseStudent(db.Model):
    __tablename__ = 'Course_student'
    course_student_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('Student.student_id'))
    course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'))
    active= db.Column(db.Boolean,default=True)

    def __init__(self, student_id, course_id, active):
        self.student_id = student_id
        self.course_id = course_id
        self.active = active

with app.app_context():
    db.create_all()

class CourseStudentSchema(ma.Schema):
    class Meta:
        fields = ('course_student_id','student_id','course_id', 'active')

