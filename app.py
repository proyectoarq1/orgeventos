from flask import Flask, render_template, make_response
from flask_restful import Resource, Api
from flask_login import login_required
from db.models import Session, Usuario, Evento
from formularios.evento_form import EventoForm
from db.adapter import adapter
import datetime
from flask import request, redirect, url_for, session
import os
from controlers.homeController import HomeController
from controlers.perfilController import PerfilController
from controlers.eventoController import EventoController
from controlers.nuevoEventoController import NuevoEventoController

app = Flask(__name__)
api = Api(app)

api.add_resource(HomeController, '/',endpoint="home")
api.add_resource(PerfilController, '/perfil',endpoint="perfil")
api.add_resource(EventoController, '/evento/<evento_id>',endpoint="evento")
api.add_resource(NuevoEventoController, '/nuevo_evento',endpoint="nuevo_evento")



if __name__ == '__main__':
	port = os.getenv('PORT', '5000')
	app.secret_key = 'super secret key'
	app.run(host='0.0.0.0',port=int(port),debug=True)
  