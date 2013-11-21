from osv import osv, fields
from openerp import tools

OCCUPATION = [
    ('1', 'Business'),
    ('2', 'Government job'),
    ('3', 'Service'),
    ('4', 'House wife'),
    ('5', 'Others')
]

BLOOD_GROUP = [
    ('a_pos', 'A+'),
    ('a_neg', 'A-'),
    ('b_pos', 'B+'),
    ('b_neg', 'B'),
    ('ab_pos', 'AB+'),
    ('ab_neg', 'AB-'),
    ('o_pos', 'O+'),
    ('o_neg', 'O-')]


class Student(osv.osv):
    _name = "school.student"

    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(
                obj.image,
                avoid_resize_medium=True
            )
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {
            'image': tools.image_resize_image_big(value)
            }, context=context
        )

    def _has_image(self, cr, uid, ids, name, args, context=None):
        result = {}
        for obj in self.browse(cr, uid, ids, context=context):
            #if obj.image:
            #    result[obj.id] = True
            #else:
            #    result[obj.id] = False
            result[obj.id] = True if obj.image else False
        return result

    def confirm_students(self, cr, uid, ids, context=None):
        vals = {}
        vals['state'] = 'confirmed'
        vals['name'] = self.pool.get('ir.sequence').get(
            cr, uid, 'student.sequence') or '/'
        self.write(cr, uid, ids, vals, context=context)

        return True

    _rec_name = "first_name"
    _columns = {
        'image': fields.binary(
            "Image", help="This field holds the image used as image"
            "for the product, limited to 1024x1024px."),
        'image_medium': fields.function(
            _get_image, fnct_inv=_set_image, string="Medium-sized image",
            type="binary", multi="_get_image", store={
                'school.student': (
                    lambda self, cr, uid, ids, c={}: ids, ['image'], 10
                ),
            },
            help="Medium-sized image of the product. It is automatically "
                 "resized as a 128x128px image, with aspect ratio preserved, "
                 "only when the image exceeds one of those sizes. Use this "
                 "field in form views or some kanban views."
        ),
        'image_small': fields.function(
            _get_image, fnct_inv=_set_image, string="Small-sized image",
            type="binary", multi="_get_image", store={
                'school.student': (
                    lambda self, cr, uid, ids, c={}: ids, ['image'], 10
                ),
            },
            help="Small-sized image of this contact. It is automatically "
                 "resized as a 64x64px image, with aspect ratio preserved. "
                 "Use this field anywhere a small image is required."
        ),
        'has_image': fields.function(_has_image, type="boolean"),
        'first_name': fields.char('Name', required=True),
        'middle_name': fields.char('Middle Name'),
        'last_name': fields.char('Last Name', required=True),
        'student_id': fields.char('Student id'),
        'school_address': fields.many2one('res.partner', 'School Address'),
        'home_address': fields.many2one('res.partner', 'Home Address'),
        'email': fields.char('Email'),
        'phone': fields.char('Phone'),
        'mobile': fields.char('Mobile'),
        'im_id': fields.char('IM id'),
        'nationality': fields.many2one('res.country', 'Nationality'),
        'date_of_birth': fields.date('Date of Birth'),
        'gender': fields.selection([('male', 'Male'),
                                   ('female', 'Female')],
                                   'Gender'),
        'mother_tongue': fields.many2one('res.lang', 'Mother Tongue'),
        'identification_no': fields.char('Identification No'),
        'father_name': fields.char('Father Name'),
        'occupation_father': fields.selection(OCCUPATION, 'Occupation'),
        'mother_name': fields.char('Mother_Name'),
        'occupation_mother': fields.selection(OCCUPATION, 'Occupation'),
        'sibling': fields.char('Sibling'),
        'school': fields.many2one('res.company', 'School'),
        'course': fields.many2one('school.course_management', 'Course'),
        'class': fields.many2one('school.class', 'Class'),
        'division': fields.char('Division'),
        'roll_no': fields.integer('RollNo'),
        'note1': fields.text('Notes'),
        'doctor': fields.char('Doctor'),
        'hospital': fields.char('Hospital'),
        'phone_doc': fields.char('Phone'),
        'bloodgroup': fields.selection(BLOOD_GROUP, 'Blood Group'),
        'weight': fields.integer('Weight (in kgs)'),
        'height': fields.integer('Height (in cms)'),
        'eyes': fields.boolean('Eyes'),
        'ears': fields.boolean('Ears'),
        'nose_throat': fields.boolean('Nose & Throat'),
        'respiratory': fields.boolean('Respiratory'),
        'cardiovascular': fields.boolean('Cardiovascular'),
        'muskoskeletal': fields.boolean('Muskoskeletal'),
        'neurological': fields.boolean('Neurological'),
        'dermatological': fields.boolean('Dermatological'),
        'blood_pressure': fields.boolean('Blood Pressure'),
        'note': fields.text('Notes'),
        'academic_history': fields.one2many('school.student_academic_history',
                                            'student', 'Academic History'),
        'state': fields.selection([('draft', 'Draft'),
                                  ('confirmed', 'Confirmed'),
                                  ('alumni', 'Alumni')], 'State'),
    }

    _defaults = {
        'state': 'draft',
    }

Student()


class Academic_History(osv.osv):
    _name = "school.student_academic_history"
    _columns = {
        'student': fields.many2one('school.student', 'Student'),
        'prev_school': fields.char("School"),
        'class': fields.char("Class"),
        'from': fields.date("From"),
        'to': fields.date("To"),
        'result': fields.char("Result"),
    }
Academic_History()
