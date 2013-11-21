from osv import osv, fields
from openerp import tools


OCCUPATION = [
    ('1', 'Business'),
    ('2', 'Government job'),
    ('3', 'Service'),
    ('4', 'House wife'),
    ('5', 'Others')
]


class Admission(osv.osv):
    _name = 'school.admission'
    _description = "Application"

    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(
                obj.image, avoid_resize_medium=True)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(
            cr, uid, [id],
            {'image': tools.image_resize_image_big(value)}, context=context)

    def _has_image(self, cr, uid, ids, name, args, context=None):
        result = {}
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = True if obj.image else False
        return result

    _rec_name = "first_name"

    _columns = {
        'image': fields.binary(
            "Image",
            help="This field holds the image used as image for applicant, "
            "limited to 1024x1024px."),
        'image_medium': fields.function(
            _get_image, fnct_inv=_set_image,
            string="Medium-sized image", type="binary", multi="_get_image",
            store={'school.admission': (lambda self, cr, uid, ids, c={}: ids,
                                        ['image'], 10), },
            help="Medium-sized image of the product. It is automatically "
            "resized as a 128x128px image, with aspect ratio preserved, "
            "only when the image exceeds one of those sizes. Use this field "
            "in form views or some kanban views."),
        'image_small': fields.function(
            _get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store={
                'school.admission': (
                    lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Small-sized image of this contact. It is automatically "
                 "resized as a 64x64px image, with aspect ratio preserved. "
                 "Use this field anywhere a small image is required."),
        'has_image': fields.function(_has_image, type="boolean"),
        'first_name': fields.char('Name', size=20, required=True),
        'middle_name': fields.char('Middle Name', size=20),
        'last_name': fields.char('Last Name', size=20, required=True),
        'admission_no': fields.char('Admission Number'),
        'admission_date': fields.date('Admission Date'),
        'school': fields.many2one('res.company', 'School'),
        'course': fields.many2one('school.course_management', 'Course'),
        'category': fields.many2one('school.admission_categ_id', 'Category'),
        'fee': fields.char('Fee Receipt'),
        'home_address': fields.many2one('res.partner', 'Home Address'),
        'email': fields.char('Email'),
        'phone': fields.char('Phone'),
        'mobile': fields.char('Mobile'),
        'father': fields.char("Father's Name"),
        'occupation_father': fields.selection(OCCUPATION, 'Occupation'),
        'mother': fields.char("Mother's Name"),
        'occupation_mother': fields.selection(OCCUPATION, 'Occupation'),
        'sibling': fields.char('Sibling'),
        'nationality': fields.many2one('res.country', 'Nationality'),
        'dob': fields.date('Date Of Birth'),
        'gender': fields.selection([('male', 'Male'),
                                   ('female', 'Female')], 'Gender'),
        'previous_education': fields.one2many(
            'school.admission_previous_education', 'admission',
            'Previous Education'),
        'note': fields.text('Note'),
        'state': fields.selection([('draft', 'Draft'),
                                   ('applied', 'Application Confirmed'),
                                   ('admitted', 'Admitted'),
                                   ('student', 'Student Created'),
                                   ('cancel', 'Cancelled')], 'State'),
    }

    _defaults = {
        'state': 'draft',
    }

    def confirm_application(self, cursor, user, ids, context=None):
        self.write(cursor, user, ids, {'state': 'applied'}, context=context)
        return True

    def confirm_admission(self, cursor, user, ids, context=None):
        vals = {}
        vals['state'] = 'admitted'
        vals['admission_no'] = self.pool.get('ir.sequence').get(
            cursor, user, 'admission.sequence') or '/'
        self.write(cursor, user, ids, vals, context=context)
        return True

    def create_students(self, cursor, user, ids, context=None):
        vals = {}
        student_obj = self.pool.get('school.student')
        print student_obj
        for admission in self.browse(cursor, user, ids, context=context):
            vals['image'] = admission.image
            vals['first_name'] = admission.first_name
            vals['middle_name'] = admission.middle_name
            vals['last_name'] = admission.last_name
            vals['home_address'] = admission.home_address.id
            vals['email'] = admission.email
            vals['phone'] = admission.phone
            vals['mobile'] = admission.mobile
            vals['nationality'] = admission.nationality.id
            vals['date_of_birth'] = admission.dob
            vals['gender'] = admission.gender
            vals['father_name'] = admission.father
            vals['mother_name'] = admission.mother
            vals['occupation_father'] = admission.occupation_father
            vals['occupation_mother'] = admission.occupation_mother
            vals['sibling'] = admission.sibling
            vals['school'] = admission.school.id

            student_id = student_obj.create(cursor, user, vals,
                                            context=context)
        if student_id:
            self.write(cursor, user, ids, {'state': 'student'},
                       context=context)
        return True

    def cancel(self, cursor, user, ids, context=None):
        self.write(cursor, user, ids, {'state': 'cancel'}, context=context)
        return True


Admission()


class PreviousEducation(osv.osv):
    _name = "school.admission_previous_education"
    _description = "Previous Education"

    _columns = {
        'institute': fields.char('Institute'),
        'degree': fields.char('Degree'),
        'from': fields.date('From'),
        'to': fields.date('To'),
        'result': fields.char('Result'),
        'admission': fields.many2one('school.admission', 'Admission'),
    }
PreviousEducation()


class AdmissionCategoryId(osv.osv):
    _name = "school.admission_categ_id"

    _columns = {
        'name':  fields.char('Name'),
        'section_id':  fields.char('Team'),
    }
AdmissionCategoryId()
