
from config.database import db, ma, app

class Admin(db.Model):
    __tablename__ = 'Admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    DNI = db.Column (db.Integer)
    name = db.Column (db.String(150))
    password = db.Column (db.String(150))
    active= db.Column(db.Boolean,default=True)
    def __init__(self, email,DNI,name,password,active):
        self.email = email
        self.DNI = DNI
        self.name = name
        self.password = password
        self.active = active

with app.app_context():
    db.create_all()


class AdminSchema(ma.Schema):
    class Meta:
        fields = ('admin_id','email','DNI','name','password')
