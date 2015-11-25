from flask import Flask, render_template, make_response, flash
from flask_restful import Resource, Api
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from db.models import Session, Evento
from formularios.evento_form import EventoForm
import datetime
from flask import request, redirect, url_for, session
import os
from db.adapter_selected import adapter
from controllers.homeController import HomeController
from controllers.registerController import RegisterController
from controllers.loginController import LoginController
from controllers.logoutController import LogoutController
from controllers.perfilController import PerfilController
from controllers.eventoController import EventoController
from controllers.editarEventoController import EditarEventoController
from controllers.nuevoEventoController import NuevoEventoController
from controllers.editarUsuarioController import EditarUsuarioController
from controllers.crearRecursoController import CrearRecursoController
from controllers.asignarRecursoController import AsignarRecursoController
from controllers.eventoYAsistenciaController import EventoYAsistenciaController
from controllers.dealerEventosController import DealerEventosController


import logging
from logging.handlers import TimedRotatingFileHandler
from logging import getLogger

UPLOAD_FOLDER = '/static/imagenes'


app = Flask(__name__)
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Necesitas estar logueado para acceder a esa pagina"

@login_manager.user_loader
def load_user(user_id):
	return adapter.get_user_by_id(user_id)

#@login_manager.unauthorized_handler
#def unauthorized():
#    return 'Loggueate capo'


@app.errorhandler(400)
def page_not_found(e):
    return render_template('login.html'),400

app.config.from_object('config')
 
app.config['SECURITY_POST_LOGIN'] = '/profile'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


api.add_resource(HomeController, '/',endpoint="home")
api.add_resource(RegisterController, '/register',endpoint="register")
api.add_resource(LoginController, '/login',endpoint="login")
api.add_resource(LogoutController, '/logout',endpoint="logout")
api.add_resource(PerfilController, '/perfil',endpoint="perfil")
api.add_resource(EditarUsuarioController, '/editarme', endpoint="editar_perfil")
api.add_resource(EventoController, '/evento/<evento_id>',endpoint="evento")
api.add_resource(EditarEventoController, '/editar/<evento_id>',endpoint="editar_evento")
api.add_resource(NuevoEventoController, '/nuevo_evento',endpoint="nuevo_evento")
api.add_resource(CrearRecursoController, '/crear_recurso',endpoint="crear_recurso")
api.add_resource(AsignarRecursoController, '/asignar_recurso', endpoint="asignar_recurso")
api.add_resource(EventoYAsistenciaController, '/evento_asistencia', endpoint="evento_asistencia")
api.add_resource(DealerEventosController, '/dealer_eventos', endpoint='dealer_eventos')


if __name__ == '__main__':
	port = os.getenv('PORT', '5000')
	app.secret_key = 'super secret key'
	app.run(host='0.0.0.0',port=int(port),debug=True)
  