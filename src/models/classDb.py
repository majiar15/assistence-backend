
from config.database import db, ma, app

class ClassDb(db.Model):
    __tablename__ = 'classDb'
    classDb_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'))
    date = db.Column(db.Date)

    def __init__(self,course_id,date):
        self.course_id = course_id
        self.date = date

with app.app_context():
    db.create_all()


class ClassDbSchema(ma.Schema):
    class Meta:
        fields = ('classDb_id','course_id','date')
