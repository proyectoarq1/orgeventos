from flask import Flask, render_template, make_response, current_app
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from flask_restful import Resource
from db.models import Evento
from formularios.evento_form import EventoForm
from db.adapter_selected import adapter
from flask import request, redirect, url_for, session
import os

class HomeController(Resource):
    def get(self):
    	current_app.logger.info('Obteniendo eventos publicos..')
    	#eventos_publicos = adapter.obtener_eventos_publicos()
    	eventos_publicos = adapter.obtener_eventos_publicos_limit(12)
    	#for e in eventos_publicos:
    	#	print e["_id"]

    	last_id = eventos_publicos[-1]["_id"]
    	primer_id = eventos_publicos[0]["_id"]
    	#print last_id
    	headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html',eventos_publicos=eventos_publicos, last_id=last_id, primer_id=primer_id),200,headers)