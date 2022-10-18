
from email.policy import default
from config.database import db, ma, app

class Student(db.Model):
    __tablename__ = 'Student'
    student_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    student_card = db.Column (db.Integer)
    DNI = db.Column (db.Integer)
    name = db.Column (db.String(150))
    active= db.Column(db.Boolean,default=True)

    def __init__(self, email, student_card, DNI, name,active):
        
        self.email = email
        self.student_card = student_card
        self.DNI = DNI
        self.name = name
        self.active=active
        
        
        

with app.app_context():
    db.create_all()


class StudentSchema(ma.Schema):
    class Meta:
        fields = ('student_id','email','student_card','DNI','name')

