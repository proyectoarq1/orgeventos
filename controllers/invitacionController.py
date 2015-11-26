from flask import render_template, make_response, request, redirect, url_for, current_app
from formularios.evento_form import EventoForm
from flask_restful import Resource
from db.adapter_selected import adapter
from flask.ext.login import login_required, current_user



class InvitacionController(Resource):
    @login_required
    def delete(self,evento_id):
        adapter.borrar_invitacion(evento_id, current_user.get_id());
        current_app.logger.info('La invitacion del evento ' + evento_id + ' fue borrado con exito')
        return "ok"