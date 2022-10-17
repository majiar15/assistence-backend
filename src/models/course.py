
from config.database import db, ma, app

class Course(db.Model):
    __tablename__ = 'Course'
    course_id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('Teacher.teacher_id'))
    name = db.Column(db.String(150))
    duration = db.Column(db.String(150))
    date_start = db.Column(db.Date)
    date_end = db.Column(db.Date)
    active= db.Column(db.Boolean,default=True)

    def __init__(self, teacher_id,name,duration,date_start,date_end,active):
        self.teacher_id = teacher_id
        self.name = name
        self.duration = duration
        self.date_start = date_start
        self.date_end = date_end,
        self.active = active

with app.app_context():
    db.create_all()


class CourseSchema(ma.Schema):
    class Meta:
        fields = ('course_id','teacher_id','name','duration','date_start','date_end')
