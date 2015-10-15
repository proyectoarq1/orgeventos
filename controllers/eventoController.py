from flask import Flask, render_template, make_response
from flask_restful import Resource
from db.adapter import adapter
from flask import session
from flask.ext.login import current_user


class EventoController(Resource):
    def get(self,evento_id):
    	evento = adapter.get_evento(current_user.id,evento_id)
    	headers = {'Content-Type': 'text/html'}
    	return make_response(render_template('evento.html',evento=evento),200,headers)