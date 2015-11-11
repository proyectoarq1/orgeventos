from flask import render_template, make_response, request, redirect, url_for
from formularios.evento_form import EventoForm
from flask_restful import Resource
from db.adapter_selected import adapter
from flask.ext.login import login_required



class EditarEventoController(Resource):
    @login_required
    def get(self,evento_id):
        evento = adapter.get_evento_object(evento_id)
        form = EventoForm(obj=evento)

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("nuevo_evento.html", action="/editar/"+evento_id, editar=True,form=form),200,headers)

    def post(self,evento_id):
    	form = EventoForm(request.form)
    	if form.validate():
    		evento = adapter.guardar_edicion_a_evento(evento_id,form)
    		return redirect(url_for('evento', evento_id=evento_id))
    	else :
    		headers = {'Content-Type': 'text/html'}
	    	return make_response(render_template('nuevo_evento.html', form=form, editar=True, action="/editar/"+evento_id),200,headers)