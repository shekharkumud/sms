from osv import osv, fields


WEEK_DAY = [
    ('mon', 'Monday'),
    ('tues', 'Tuesday'),
    ('wed', 'Wednesday'),
    ('thurs', 'Thursday'),
    ('fri', 'Friday'),
    ('sat', 'Saturday'),
]


class FacultySchedule(osv.osv):
    _name = "school.faculty_schedule"
    _rec_name = "faculty"

    _columns = {
        'faculty': fields.many2one('school.faculty', 'Faculty Name'),
        'academic_year': fields.many2one('school.academic_year',
                                         'Academic Year'),
        'school': fields.many2one('res.company', 'School'),
        'semester': fields.many2one('school.semester', 'Semester'),
        'notes': fields.text('Notes'),
        'time_table': fields.one2many('school.faculty_time_table',
                                      'faculty_time_table', 'Time-Table'),
    }

FacultySchedule()


class Timetable(osv.osv):
    _name = "school.faculty_time_table"

    _columns = {
        'faculty_time_table': fields.many2one('school.faculty_schedule',
                                              'Time-Table'),
        'week_day': fields.selection(WEEK_DAY, 'Week Day'),
        'subject': fields.many2one('school.subjects', 'Subject'),
        'classes': fields.many2one('school.class', 'Class'),
        'division': fields.char('Division', size=5),
        'start_time': fields.float('Start Time', size=10),
        'end_time': fields.float('End Time', size=10),
    }
Timetable()


class Class(osv.osv):
    _name = "school.class_schedule"
    _rec_name = "classes"

    _columns = {
        'classes': fields.many2one('school.class', 'Class'),
        'academic_year': fields.many2one('school.academic_year',
                                         'Academic Year'),
        'school': fields.many2one('res.company', 'School'),
        'course': fields.many2one('school.course_management', 'Course'),
        'division': fields.char('Division', size=5),
        'semester': fields.many2one('school.semester', 'Semester'),
        'time_table': fields.one2many('school.class_time_table',
                                      'class_time_table', 'Time-Table'),
        'note': fields.text('Note'),
    }

    def confirm_schedule(self, cursor, user, ids, context=None):
        vals = {}
        schedule_obj = self.pool.get("school.faculty_schedule")
        faculty_time_table = self.pool.get("school.faculty_time_table")

        for class_schedule in self.browse(cursor, user, ids, context=context):
            for time_table in class_schedule.time_table:
                vals = {
                    'week_day': time_table.week_day,
                    'subject': time_table.subject.id,
                    'classes': class_schedule.classes.id,
                    'division': class_schedule.division,
                    'start_time': time_table.start_time,
                    'end_time': time_table.end_time,
                }
                faculty = time_table.faculty.id
                start_time = time_table.start_time
                print faculty
                print time_table.faculty.first_name
                faculty_schedule_ids = schedule_obj.search(cursor, user,
                                                           [('faculty', '=',
                                                            faculty)],
                                                           context=context)
                print faculty_schedule_ids
                if faculty_schedule_ids and (len(faculty_schedule_ids) == 1):
                    faculty_time_ids = faculty_time_table.search(
                        cursor, user, [('start_time', '=', start_time)],
                        context=context)
                    if faculty_time_ids:
                        pass
                        print "Same Record"
                    else:
                        vals['faculty_time_table'] = (faculty_schedule_ids[0]
                                                      or faculty_schedule_ids,)
                        print "New REcord"
                elif not faculty_schedule_ids:
                    faculty_schedule_new_id = schedule_obj.create(
                        cursor, user,
                        {
                            'faculty': faculty,
                            'academic_year': class_schedule.academic_year.id,
                            'school': class_schedule.school.id,
                            'semester': class_schedule.semester.id,
                        },
                        context=context)
                    print faculty_schedule_new_id
                    vals['faculty_time_table'] = faculty_schedule_new_id
                else:
                    pass
                print vals
                faculty_time_table.create(cursor, user, vals, context=context)

        return None

Class()


class Timetable(osv.osv):
    _name = "school.class_time_table"

    _columns = {
        'class_time_table': fields.many2one('school.class_schedule',
                                            'Time-Table'),
        'week_day': fields.selection(WEEK_DAY, 'Week Day'),
        'subject': fields.many2one('school.subjects', 'Subject'),
        'faculty': fields.many2one('school.faculty', 'Faculty'),
        'start_time': fields.float('Start Time', size=10),
        'end_time': fields.float('End Time', size=10),
    }
Timetable()
