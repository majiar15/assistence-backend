
from config.database import db, ma, app

class ClassDb(db.Model):
    __tablename__ = 'ClassDb'
    classDb_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'))
    date = db.Column(db.Date)
    active= db.Column(db.Boolean,default=True)

    def __init__(self,course_id,date,active):
        self.course_id = course_id
        self.date = date
        self.active = active

with app.app_context():
    db.create_all()


class ClassDbSchema(ma.Schema):
    class Meta:
        fields = ('classDb_id','course_id','date')
