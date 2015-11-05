
from wtforms import Form, TextField, PasswordField, validators
from wtforms.fields.html5 import DateField

class UserForm(Form):

    username = TextField('Nombre de usuario', [validators.Length(min=4, max=25),validators.Required(message="Por favor ingrese el nombre del evento.")])
    email = TextField('Email Address', [validators.Regexp('[\w.-]+@[\w.-]+', flags=0, message='Por favor ingrese una direccion de e-mail valida')])
    password = PasswordField('Password', [validators.Length(min=6, max=25, message="La password debe tener como mino seis caracteres"),validators.Required(message='Debe ingresar una password'),validators.EqualTo('confirm', message='Las passwords deben coincidir')])
    confirm = PasswordField('Por favor repita la password',[validators.Required(message='Debe confirmar la password ingresada')])

if __name__ == '__main__':
	#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dbsettings")
	#session = Session()
	pass