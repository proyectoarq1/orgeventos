from db.models import Session
from wtforms.validators import ValidationError

class Unique(object):
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = u'el valor ingresado ya existe'
        self.message = message

    def __call__(self, form, field):
        db_session=Session()
        check = db_session.query(self.model).filter(self.field==field.data).first() 
        #check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)