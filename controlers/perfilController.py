from flask import Flask, render_template, make_response
from flask_restful import Resource
from db.adapter import adapter
from flask import session


class PerfilController(Resource):
    def get(self):
    	usuario = adapter.get_usuario(session['usuario_id'])
    	eventos = adapter.obtener_eventos_asignados(session['usuario_id'])
    	headers = {'Content-Type': 'text/html'}
    	return make_response(render_template('perfil.html',usuario=usuario, eventos=eventos),200,headers)