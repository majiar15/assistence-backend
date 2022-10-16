
from config.database import db, ma, app

class Teacher(db.Model):
    __tablename__ = 'Teacher'
    teacher_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    DNI = db.Column (db.Integer)
    name = db.Column (db.String(150))
    password = db.Column (db.String(150))

    def __init__(self, email,DNI,name,password):
        self.email = email
        self.DNI = DNI
        self.name = name
        self.password = password

with app.app_context():
    db.create_all()


class TeacherSchema(ma.Schema):
    class Meta:
        fields = ('teacher_id','email','DNI','name','password')
