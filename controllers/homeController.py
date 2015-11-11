from flask import Flask, render_template, make_response
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from flask_restful import Resource
from db.models import Evento
from formularios.evento_form import EventoForm
from db.adapter_selected import adapter
from flask import request, redirect, url_for, session
import os

class HomeController(Resource):
    def get(self):
    	eventos_publicos = adapter.obtener_eventos_publicos()
    	headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html',eventos_publicos=eventos_publicos),200,headers)