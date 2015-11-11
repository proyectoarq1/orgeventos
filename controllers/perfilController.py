from flask import Flask, render_template, make_response, flash, request
from flask_restful import Resource
from db.adapter_selected import adapter
from flask import session
from flask.ext.login import current_user, login_required



class PerfilController(Resource):
	@login_required
	def get(self):
		usuario = adapter.get_userJson_by_id(current_user.get_id())
		eventos = adapter.obtener_eventos_asignados(current_user.get_id())
		eventos_invitados = adapter.obtener_eventos_invitados(current_user.get_id())
		eventos_publicos = adapter.obtener_eventos_publicos()
		headers = {'Content-Type': 'text/html'}
		return make_response(render_template('perfil.html',usuario=usuario, eventos=eventos, eventos_publicos=eventos_publicos,eventos_invitados=eventos_invitados),200,headers)

	def post(self):
		resp = request.form['asistir']
		if resp[2] == "1":
			print int(resp[0])
			print current_user.get_id()
			#adapter.confirmar_asistencia_a_evento(current_user.get_id(),resp[0])
		else:
			#adapter.rechazar_asistencia_a_evento(current_user.get_id(),int(resp[0]))
			print "no asiste"
