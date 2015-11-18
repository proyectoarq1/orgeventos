
from flask import Flask, render_template, make_response,current_app, url_for, abort, flash
from flask_restful import Resource
from db.adapter_selected import adapter
from flask import session, request, redirect, json
from flask.ext.login import current_user, login_required
from formularios.requerimientoForm import RequerimientoForm


class CrearRecursoController(Resource):
    
    @login_required
    def post(self):
    	form = RequerimientoForm(request.form)

        evento_id = request.form["evento_id"]
        if form.validate():
            requerimiento = adapter.crear_requerimiento(evento_id,form)
            return requerimiento

    @login_required
    def put(self):
        form = RequerimientoForm(request.form)
        if form.validate():
            requerimiento = adapter.guardar_edicion_a_requerimiento(request.form["recurso_id"],form)

            return requerimiento

    @login_required
    def delete(self):
        recurso_id = request.form["id_recurso"]
        adapter.borrar_requerimiento(recurso_id)
        return recurso_id
            


