

from wtforms import Form, BooleanField, TextField, validators, SelectField
from wtforms.fields.html5 import DateField

class EventoForm(Form):
    nombre = TextField('Nombre evento', [validators.Length(min=4, max=100),validators.Required(message="Por favor ingrese el nombre del evento.")])
    fecha = TextField('Fecha del evento', [validators.Regexp('(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}', flags=0, message='Por favor ingrese una fecha valida con formato dd/mm/aaaa')])
    hora = TextField('Hora del evento', [validators.Regexp('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', flags=0, message='Por favor ingrese una hora valida con formato hh:mm')]) 
    descripcion = TextField('Descripcion del evento', [validators.Length(min=0, max=700)])
    url_imagen = TextField('URL imagen', [validators.Regexp('(^$|(http?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', flags=0, message='Por favor ingrese una URL de imagen que comience con http://')]) 
    ubicacion = TextField('Ciudad',[validators.Required(message="Por favor ingrese el nombre de una ciudad.")])
    categoria = SelectField('Categoria',choices=[('Publico', 'Publico'), ('Privado', 'Privado')])

if __name__ == '__main__':
	#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dbsettings")
	#session = Session()
	e = EventoForm(nombre="jajaja")
	
	print e.nombre.data