from flask import Flask, render_template, make_response, url_for
from formularios.evento_form import EventoForm
from flask_restful import Resource
from db.adapter_selected import adapter
from flask import session, request, redirect
from flask.ext.login import current_user


class NuevoEventoController(Resource):
    def get(self):
    	form = EventoForm(request.form)
    	headers = {'Content-Type': 'text/html'}
    	return make_response(render_template('nuevo_evento.html', form=form, method="post", action="/nuevo_evento"),200,headers)

    def post(self):
    	form = EventoForm(request.form)
    	if form.validate():
    		adapter.crear_evento(current_user.get_id(),form)
    		return redirect(url_for('perfil'))
    	else :
    		headers = {'Content-Type': 'text/html'}
	    	return make_response(render_template('nuevo_evento.html', form=form, method="post", action="/nuevo_evento"),200,headers)
