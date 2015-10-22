
from wtforms import Form, BooleanField, TextField, validators, SelectField
from wtforms.fields.html5 import DateField

class EventoForm(Form):
    nombre = TextField('Nombre evento', [validators.Length(min=4, max=25),validators.Required(message="Por favor ingrese el nombre del evento.")])
    #fecha = DateField('Fecha del evento', [validators.Required(message="Por favor ingrese una fecha valida con formato dd/mm/aaaa")])
    fecha = TextField('Fecha del evento', [validators.Regexp('(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}', flags=0, message='Por favor ingrese una fecha valida con formato dd/mm/aaaa')]) 
    hora = TextField('Hora del evento', [validators.Regexp('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', flags=0, message='Por favor ingrese una hora valida con formato hh:mm')]) 
    descripcion = TextField('Descripcion del evento', [validators.Length(min=4, max=200),validators.Required(message="Por favor ingrese una descripcion para el evento")])
    ubicacion = TextField('Ubicacion del evento', [validators.Length(min=5, max=500),validators.Required(message="Por favor ingrese una ubicacion para el evento")])
    categoria = SelectField('Categoria',choices=[('Publico', 'Publico'), ('Privado', 'Privado')])

if __name__ == '__main__':
	#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dbsettings")
	#session = Session()
	e = EventoForm(nombre="jajaja")
	
	print e.nombre.data