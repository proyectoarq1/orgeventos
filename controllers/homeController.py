from flask import Flask, render_template, make_response
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required, current_user
from flask_restful import Resource
from db.models import Usuario, Evento
from formularios.evento_form import EventoForm
from db.adapter import adapter
from flask import request, redirect, url_for, session
import os

def hacer_usuario_y_ejemplo():
	
	usuario = adapter.crear_usuario("Cosme Fulanito")
	usuario_id = adapter.get_id(usuario)

	form_evento1 = EventoForm(nombre="Evento uno", fecha=None, descripcion="Me gustaria poder organizar una juntada")
	form_evento2 = EventoForm(nombre="Evento dos", fecha=None, descripcion="Hagamos tambien otra juntada mas")

	e1 = adapter.crear_evento(usuario_id,form_evento1)
	e2 = adapter.crear_evento(usuario_id,form_evento2)

	
	session['usuario_id'] = usuario_id

class HomeController(Resource):
    def get(self):
    	headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html'),200,headers)