
from flask import Flask, render_template, make_response,current_app, url_for, abort, flash
from flask_restful import Resource
from db.adapter_selected import adapter
from flask import session, request, redirect
from flask.ext.login import current_user, login_required
from formularios.requerimientoForm import RequerimientoForm


class CrearRecursoController(Resource):
    
    @login_required
    def post(self,evento_id):
    	form = RequerimientoForm(request.form)
    	if form.validate():
            print "hasta aca llegue carajo"
            adapter.crear_requerimiento(evento_id,form)
            return redirect(url_for('evento',evento_id=evento_id))
        else:
            current_app.logger.error('login user')
            flash('Alguno de los datos ingresados para crear un requerimiento son invalidos' , 'error')
            return redirect(url_for('evento',evento_id=evento_id))

    def delete(self,recurso_id):
        adapter.borrar_requerimiento(recurso_id)
        flash('El requerimiento ha sido correctamente borrado' , 'info')
        return redirect(url_for('evento',evento_id=evento_id))
            


