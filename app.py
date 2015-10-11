from flask import Flask, render_template, make_response
from flask_restful import Resource, Api
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from db.models import Session, Usuario, Evento
from formularios.evento_form import EventoForm
from db.adapter import adapter
import datetime
from flask import request, redirect, url_for, session
import os
from controlers.homeController import HomeController
from controlers.registerController import RegisterController
from controlers.loginController import LoginController
from controlers.logoutController import LogoutController
from controlers.perfilController import PerfilController
from controlers.eventoController import EventoController
from controlers.nuevoEventoController import NuevoEventoController
import logging
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	return adapter.get_user_by_id(user_id)

#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('login.html'), 404

app.config.from_object('config')
 
app.config['SECURITY_POST_LOGIN'] = '/profile'

formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
file_handler = TimedRotatingFileHandler(app.config['LOG_PATH'], when="D", backupCount=7)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

api.add_resource(HomeController, '/',endpoint="home")
api.add_resource(RegisterController, '/register',endpoint="register")
api.add_resource(LoginController, '/login',endpoint="login")
api.add_resource(LogoutController, '/logout',endpoint="logout")
api.add_resource(PerfilController, '/perfil',endpoint="perfil")
api.add_resource(EventoController, '/evento/<evento_id>',endpoint="evento")
api.add_resource(NuevoEventoController, '/nuevo_evento',endpoint="nuevo_evento")



if __name__ == '__main__':
	port = os.getenv('PORT', '5000')
	app.secret_key = 'super secret key'
	app.run(host='0.0.0.0',port=int(port),debug=True)
  