from flask import Flask, render_template, make_response, flash, request, json, current_app
from flask_restful import Resource
from db.adapter_selected import adapter
from flask import session
from flask.ext.login import current_user, login_required
from db.utils.Asistencia import *



class PerfilController(Resource):
	@login_required
	def get(self):
		usuario = adapter.get_userJson_by_id(current_user.get_id())

		current_app.logger.info('Obnetiendo eventos propios para cargar en el perfil')
		eventos = adapter.obtener_eventos_asignados(current_user.get_id())[:5]
		last_id_propios = 0
		primer_id_propios = 0

		if eventos != []:
			last_id_propios = eventos[-1]["_id"]
			primer_id_propios = eventos[0]["_id"]

		current_app.logger.info('Obnetiendo eventos a los que el usuario esta invitado para cargar en el perfil')
		eventos_invitados = adapter.obtener_eventos_invitados(current_user.get_id())[:5]
		last_id_invitados = 0
		primer_id_invitados = 0

		if eventos_invitados != []:
			last_id_invitados = eventos_invitados[-1]["_id"]
			primer_id_invitados = eventos_invitados[0]["_id"]

		headers = {'Content-Type': 'text/html'}
		return make_response(render_template('perfil.html', primer_id_propios=primer_id_propios,last_id_propios=last_id_propios, primer_id_invitados=primer_id_invitados, last_id_invitados=last_id_invitados, usuario=usuario, eventos=eventos,eventos_invitados=eventos_invitados),200,headers)

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
