
from wtforms import Form, BooleanField, TextField, validators, SelectField, IntegerField
from wtforms.fields.html5 import DateField

class RequerimientoForm(Form):
    nombre = TextField('Nombre del requerimiento', [validators.Length(min=4, max=25),validators.Required(message="Por favor ingrese el nombre del requerimiento. Ej: 'Coca-cola'")])
    descripccion = TextField('Descripcion del requerimiento', [validators.Length(min=4, max=200),validators.Required(message="Por favor ingrese una descripcion para el requerimiento. Ej:'Necesitamos coca para el fernet' ")])
    cantidad = IntegerField('Cantidad del requerimiento, como minimo cero', [validators.Required(message="Por favor ingrese una cantidad para el requerimiento")])

if __name__ == '__main__':
	#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dbsettings")
	#session = Session()
	e = EventoForm(nombre="jajaja")
	
	#print e.nombre.data^[1-9][0-9][0-9][0-9]