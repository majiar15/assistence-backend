from models.admin import AdminSchema,Admin
from models.teacher import TeacherSchema,Teacher

from models.cource import CourseSchema,Course
from models.schedule import ScheduleSchema,Schedule
from models.classDb import ClassDbSchema,ClassDb

from models.student import StudentSchema,Student
from models.course_student import CourseStudentSchema,CourseStudent
from models.asisst import AsisstSchema,Asisst


Admin_schema = AdminSchema()
Admins_schema = AdminSchema(many=True)

teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many=True)

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)

schedule_schema = ScheduleSchema()
schedules_schema = ScheduleSchema(many=True)

classDb_schema = ClassDbSchema()
classDbs_schema = ClassDbSchema(many=True)

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

course_student_schema = CourseStudentSchema()
course_students_schema = CourseStudentSchema(many=True)

asisst_schema = AsisstSchema()
asissts_schema = AsisstSchema(many=True)