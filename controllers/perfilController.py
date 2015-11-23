from flask import Flask, render_template, make_response, flash, request, json
from flask_restful import Resource
from db.adapter_selected import adapter
from flask import session
from flask.ext.login import current_user, login_required
from db.utils.Asistencia import *



class PerfilController(Resource):
	@login_required
	def get(self):
		eventos_invitados_y_asistencia = []
		usuario = adapter.get_userJson_by_id(current_user.get_id())
		eventos = adapter.obtener_eventos_asignados(current_user.get_id())
		eventos_invitados = adapter.obtener_eventos_invitados(current_user.get_id())
		print eventos_invitados
		for ev in eventos_invitados:
			asistencia_actual = adapter.obtener_asistencia_a_evento(ev['id'], usuario['id'])
			eventos_invitados_y_asistencia = eventos_invitados_y_asistencia + [{"evento":ev, "asistencia":asistencia_actual}] 
		eventos_publicos = adapter.obtener_eventos_publicos()
		headers = {'Content-Type': 'text/html'}
		return make_response(render_template('perfil.html', Asistencia=Asistencia, eventos_invitados_y_asistencia=eventos_invitados_y_asistencia, usuario=usuario, eventos=eventos, eventos_publicos=eventos_publicos,eventos_invitados=eventos_invitados),200,headers)

	def post(self):
		resp = request.form['asistir']
		if resp[2] == "1":
			print int(resp[0])
			print current_user.get_id()
			adapter.responder_asistencia_a_evento(resp[0], current_user.get_id(), Asistencia.Pendiente)
		else:
			if resp[2] == "2":
				adapter.responder_asistencia_a_evento(resp[0], current_user.get_id(), Asistencia.Asisto)
				print "no asiste"
			else:
				adapter.responder_asistencia_a_evento(resp[0], current_user.get_id(), Asistencia.NoAsisto)
		return json.dumps({"nothing to see": "this isn't happening"})
