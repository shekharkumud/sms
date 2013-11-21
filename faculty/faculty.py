from osv import osv, fields
from openerp import tools


class Faculty(osv.osv):
    _name = "school.faculty"

    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(
                obj.image,
                avoid_resize_medium=True)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {
            'image': tools.image_resize_image_big(value)}, context=context)

    def _has_image(self, cr, uid, ids, name, args, context=None):
        result = {}
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = True if obj.image else False
        return result

    _rec_name = "first_name"
    _columns = {
        'image': fields.binary(
            "Image",
            help="This field holds the image used as image for faculty, "
            "limited to 1024x1024px."),
        'image_medium': fields.function(
            _get_image, fnct_inv=_set_image,
            string="Medium-sized image", type="binary", multi="_get_image",
            store={'school.faculty': (lambda self, cr, uid, ids, c={}: ids,
                   ['image'], 10), }, ),
        'image_small': fields.function(
            _get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store={
                'school.faculty': (
                    lambda self, cr, uid, ids, c={}: ids, ['image'], 10
                ),
            },
            help="Small-sized image of this contact. It is automatically "
                 "resized as a 64x64px image, with aspect ratio preserved. "
                 "Use this field anywhere a small image is required."),
        'has_image': fields.function(_has_image, type="boolean"),
        'first_name': fields.char("Name", required='True'),
        'middle_name': fields.char("Middle Name"),
        'last_name': fields.char("Last Name", required='True'),
        'faculty_id': fields.char("Faculty Id", required='True'),
        'user': fields.many2one("res.users", "User"),

        #Contact Info
        'school_address': fields.many2one("res.partner", "School address"),
        'home_address': fields.many2one("res.partner", "Home address"),
        'e_mail': fields.char("E-Mail"),
        'phone': fields.char("Phone"),
        'mobile': fields.char("Mobile"),
        'imid': fields.char("IM-Id"),

        #Demographic Info
        'nationalty': fields.many2one("res.country", "Nationalty"),
        'd_o_b': fields.date("Date of Birth"),
        'gender': fields.selection([('male', 'Male'),
                                    ('female', 'Female')], 'Gender'),
        'mother_tongue': fields.char("Mother Tongue"),
        'marital_status': fields.selection([('1', 'Single'),
                                            ('2', 'Married'),
                                            ('3', 'Widower'),
                                            ('4', 'Divorced')], 'Marital'),
        'id_no': fields.char("Identification No."),

        #School Info
        'school': fields.many2one("res.company", "School"),
        'department': fields.char("Department"),
        'designation': fields.char("Designation"),
        'note': fields.text("Notes"),
        'academic_history': fields.one2many('school.faculty_academic_history',
                                            'faculty', 'Academic History'),
        'certification': fields.one2many('school.faculty_certification',
                                         'faculty', 'Certification'),
    }

Faculty()


class Academic_History(osv.osv):
    _name = "school.faculty_academic_history"
    _columns = {
        'faculty': fields.many2one('school.faculty', 'Faculty'),
        'institute': fields.char("Institute"),
        'degree': fields.char("Degree"),
        'from': fields.date("From"),
        'to': fields.date("To"),
        'result': fields.char("Result"),
    }
Academic_History()


class Certification(osv.osv):
    _name = "school.faculty_certification"
    _columns = {
        'faculty': fields.many2one('school.faculty', 'Faculty'),
        'name': fields.char("Name"),
        'institute': fields.char("Institute"),
        'valid_upto': fields.date("Valid upto"),
    }
Certification()
