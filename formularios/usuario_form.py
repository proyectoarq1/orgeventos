
from wtforms import Form, TextField, PasswordField, validators
from wtforms.fields.html5 import DateField
from our_validators.unique_validator import Unique
from db.models import User

class UserForm(Form):

    username = TextField('Nombre de usuario', [validators.Length(min=4, max=25),validators.Required(message="Por favor ingrese un nombre de usuario."),Unique(User, User.username,message="El username ya esta usado, elija otro")])
    email = TextField('Email Address', [validators.Regexp('[\w.-]+@[\w.-]+', flags=0, message='Por favor ingrese una direccion de e-mail valida'),Unique(User, User.email,message="El email ya esta usado, elija otro")])
    password = PasswordField('Password', [validators.Length(min=6, max=25, message="La password debe tener como mino seis caracteres"),validators.Required(message='Debe ingresar una password'),validators.EqualTo('confirm', message='Las passwords deben coincidir')])
    confirm = PasswordField('Por favor repita la password',[validators.Required(message='Debe confirmar la password ingresada')])

if __name__ == '__main__':
	#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dbsettings")
	#session = Session()
	pass