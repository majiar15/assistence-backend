

from config.database import app
from modules.admin.routes import admin
from modules.students.route import student
from modules.courses.route import course
from modules.schedule.route import schedule
from modules.teacher.routes import teacher
from modules.auth.routes import auth
from modules.assistance.route import assistance



app.register_blueprint(admin)
app.register_blueprint(teacher)
app.register_blueprint(auth)
app.register_blueprint(student)
app.register_blueprint(course)
app.register_blueprint(schedule)
app.register_blueprint(assistance)

### end swagger specific ###
if __name__ == '__main__':
    app.run(debug=True)
 