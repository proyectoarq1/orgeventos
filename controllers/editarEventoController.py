from flask import render_template, make_response, request, redirect, url_for, current_app
from formularios.evento_form import EventoForm
from flask_restful import Resource
from db.adapter_selected import adapter
from flask.ext.login import login_required, current_user



class EditarEventoController(Resource):
    @login_required
    def get(self,evento_id):
        evento = adapter.get_evento_object(evento_id)
        form = EventoForm(obj=evento)
        splited = str(form.fecha.data).split("-")
        nueva_fecha = splited[1] + "/"+ splited[2] + "/"+ splited[0]
        form.fecha.data = nueva_fecha

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("nuevo_evento.html", evento_id=evento_id,action="/editar/"+evento_id, editar=True,form=form),200,headers)

    @login_required
    def post(self,evento_id):
    	form = EventoForm(request.form)
    	if form.validate():
            evento = adapter.guardar_edicion_a_evento(evento_id,form)
            current_app.logger.info('Guardando edicion del evento')
            return redirect(url_for('evento', evento_id=evento_id))
    	else:
            current_app.logger.error('La edicion del evento no pudo guardarse porque el formulario no esta validado')
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('nuevo_evento.html', form=form, editar=True, action="/editar/"+evento_id),200,headers)

    @login_required
    def delete(self,evento_id):
        adapter.borrar_evento(current_user.get_id(),evento_id);
        current_app.logger.info('El evento ' + evento_id + ' fue borrado con exito')
        return "ok"
