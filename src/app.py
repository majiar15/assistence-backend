
from flask_cors import CORS

from config.database import app
from modules.admin.routes import admin

CORS(app)


app.register_blueprint(admin)


### end swagger specific ###
if __name__ == '__main__':
    app.run(debug=True)
 