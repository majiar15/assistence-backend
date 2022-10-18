
from config.database import db, ma, app

class Schedule(db.Model):
    __tablename__ = 'Schedule'
    schedule_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'))
    day = db.Column(db.String(150))
    time_start = db.Column(db.String(30))
    time_end = db.Column(db.String(30))
    active= db.Column(db.Boolean,default=True)

    def __init__(self,course_id, day, time_start, time_end,active):
        self.course_id = course_id
        self.day = day
        self.time_start = time_start
        self.time_end = time_end
        self.active = active

with app.app_context():
    db.create_all()


class ScheduleSchema(ma.Schema):
    class Meta:
        fields = ('schedule_id','course_id','day','time_start','time_end', 'active')
