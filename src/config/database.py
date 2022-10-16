from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/assistence'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# settings
app.secret_key = "zt7K9XU$P4x!"

#trabajamos con la bd 
db = SQLAlchemy(app)

ma = Marshmallow(app)