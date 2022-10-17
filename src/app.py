
from flask_cors import CORS

from config.database import app
from modules.admin.routes import admin
from modules.students.route import student
from modules.courses.route import course
from modules.schedule.route import schedule

CORS(app)


app.register_blueprint(admin)
app.register_blueprint(student)
app.register_blueprint(course)
app.register_blueprint(schedule)

### end swagger specific ###
if __name__ == '__main__':
    app.run(debug=True)
 