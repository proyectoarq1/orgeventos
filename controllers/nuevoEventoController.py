from flask import Flask, render_template, make_response, url_for
from formularios.evento_form import EventoForm
from flask_restful import Resource
from db.adapter import adapter
from flask import session, request, redirect


class NuevoEventoController(Resource):
    def get(self):
    	form = EventoForm(request.form)
    	headers = {'Content-Type': 'text/html'}
    	return make_response(render_template('nuevo_evento.html', form=form),200,headers)

    def post(self):
    	form = EventoForm(request.form)
    	adapter.crear_evento(session['user_id'],form)
    	return redirect(url_for('perfil'))
