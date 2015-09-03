
from wtforms import Form, BooleanField, TextField, validators
from wtforms.fields.html5 import DateField

class EventoForm(Form):
    nombre = TextField('Nombre evento', [validators.Length(min=4, max=25),validators.Required()])
    fecha = DateField('Fecha del evento', [validators.Required()]) 
    descripcion = TextField('Descripcion del evento', [validators.Length(min=4, max=200),validators.Required()])