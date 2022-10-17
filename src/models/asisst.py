
from config.database import db, ma, app

class Asisst(db.Model):
    __tablename__ = 'Asisst'
    asisst_id = db.Column(db.Integer, primary_key=True)
    schedule_id =  db.Column(db.Integer, db.ForeignKey('Schedule.schedule_id'))
    student_id = db.Column(db.Integer, db.ForeignKey('Student.student_id'))
    

    def __init__(self,schedule_id, student_id):
        self.schedule_id = schedule_id
        self.student_id = student_id

with app.app_context():
    db.create_all()


class AsisstSchema(ma.Schema):
    class Meta:
        fields = ('asisst_id','schedule_id','student_id')
