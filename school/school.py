# In this file, the common objects have been included. These common objects
# can be later on expanded more to their full functionality in seperate
# class files.

# 1. course management
# 2. School Subjects
# 3. school.academic_year
# 4. school.semester
# 5  class - school.class

from osv import osv, fields


class CourseManagement(osv.osv):
    _name = "school.course_management"
    _description = "Course Management"

    _columns = {
        'name': fields.char('Course', size=30),
        'course_id': fields.char('Course Id'),
    }
CourseManagement()


class Schoolsubject(osv.osv):
    _name = "school.subjects"

    _columns = {
        'name': fields.char('Subject Name', size=20),
        'code': fields.char('Subject Code', size=10),
    }
Schoolsubject()


class SchoolAcademicYear(osv.osv):
    _name = 'school.academic_year'

    _columns = {
        'name': fields.char('Academic Year', size=10),
        'start_date': fields.date('Start Date'),
        'end_date': fields.date('End Date'),
        'semesters': fields.one2many('school.semester', 'academic_year',
                                     'Semesters'),
    }
SchoolAcademicYear()


class SchoolSemester(osv.osv):
    _name = 'school.semester'

    _columns = {
        'name': fields.char('Semester Name', size=20),
        'start_date': fields.date('Start Date'),
        'end_date': fields.date('End Date'),
        'academic_year': fields.many2one('school.academic_year',
                                         'Academic Year'),
    }

SchoolSemester()


class SchoolClass(osv.osv):
    _name = 'school.class'

    _columns = {
        'name': fields.char('Class Name', size=20),
    }
SchoolClass()
