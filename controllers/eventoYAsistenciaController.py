from flask import Flask, render_template, make_response, flash, request, json
from flask_restful import Resource
from db.adapter_selected import adapter
from flask import session
from flask.ext.login import current_user, login_required
from db.utils.Asistencia import *



class EventoYAsistenciaController(Resource):

	def post(self):
		id_evento = request.form['id_evento']
		resp = request.form['asistir']
		asistencia_actual = Asistencia(resp)
		adapter.responder_asistencia_a_evento_por_id(id_evento, current_user.get_id(), asistencia_actual)
		return {'asistencia_actual': asistencia_actual.name, 'usuario': current_user.username}