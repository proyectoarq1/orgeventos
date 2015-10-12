from flask import Flask, render_template, make_response, flash
from flask_restful import Resource
from db.adapter import adapter
from flask import session
from flask.ext.login import current_user


class PerfilController(Resource):
    def get(self):
    	flash(current_user.username)

    	usuario = adapter.get_usuario(session['usuario_id'])
    	eventos = adapter.obtener_eventos_asignados(session['usuario_id'])
    	headers = {'Content-Type': 'text/html'}
    	return make_response(render_template('perfil.html',usuario=usuario, eventos=eventos),200,headers)