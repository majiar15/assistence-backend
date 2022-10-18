
from config.database import db, ma, app

class Asisst(db.Model):
    __tablename__ = 'Asisst'
    asisst_id = db.Column(db.Integer, primary_key=True)
    classDb_id =  db.Column(db.Integer, db.ForeignKey('ClassDb.classDb_id'))
    student_id = db.Column(db.Integer, db.ForeignKey('Student.student_id'))
    active= db.Column(db.Boolean,default=True)
    

    def __init__(self,classDb_id, student_id, active):
        self.classDb_id = classDb_id
        self.student_id = student_id
        self.active = active

with app.app_context():
    db.create_all()


class AsisstSchema(ma.Schema):
    class Meta:
        fields = ('asisst_id','classDb_id','student_id')
