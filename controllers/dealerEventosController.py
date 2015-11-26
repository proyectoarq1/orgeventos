from flask import Flask, render_template, make_response, current_app
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from flask_restful import Resource
from db.models import Evento
from formularios.evento_form import EventoForm
from db.adapter_selected import adapter
from flask import request, redirect, url_for, session
import os

class DealerEventosController(Resource):
    def post(self):
        tipo = request.form['tipo']
        pivote_id = request.form['pivote_id']
        pre_post = request.form['pre_post']

    	eventos = adapter.obtener_eventos_tipo_pivote_id_lugar(tipo,pivote_id,pre_post,current_user.get_id())

        if eventos==[]:
            ultimo_id = pivote_id
            primer_id = pivote_id
            if pre_post=="post":
                primer_id=int(primer_id)+1
            else:
                ultimo_id=int(ultimo_id)-1

            return {"hay_eventos":"false","ultimo_id":ultimo_id, "primer_id":primer_id}
        
        ultimo_id = eventos[-1]["_id"]
        primer_id = eventos[0]["_id"]
    	
        return {"hay_eventos":"true","eventos":eventos,"ultimo_id":ultimo_id, "primer_id":primer_id}


