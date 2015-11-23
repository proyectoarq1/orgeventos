from flask import Flask, render_template, make_response, redirect, url_for, current_app
from flask_restful import Resource
from db.adapter_selected import adapter
from flask import session,request
from flask.ext.login import current_user, login_required
from servicios.openWeatherMapAdapter import OpenWeatherMapAdapter
import urllib2, json
from db.utils.Asistencia import *
from formularios.requerimientoForm import RequerimientoForm

openweathermap = OpenWeatherMapAdapter()



class EventoController(Resource):
    
    @login_required
    def get(self,evento_id):
        evento = adapter.get_evento(evento_id)

        puede_editar= str(current_user.id == evento["organizador_id"]).lower()

        asistencia_actual = adapter.obtener_asistencia_a_evento(evento_id, current_user.id)

        clima_actual = openweathermap.get_clima(evento["ubicacion"])
        all_users = adapter.get_all_users()
        
        current_app.logger.info('Obteniendo usuarios confirmados...')
        usuarios_confirmados = adapter.obtener_usuarios_invitados_evento(evento_id,Asistencia.Asisto)

        current_app.logger.info('Obteniendo usuarios pendientes...')
        usuarios_pendientes = adapter.obtener_usuarios_invitados_evento(evento_id,Asistencia.Pendiente)

        current_app.logger.info('Obteniendo usuarios rechazados...')
        usuarios_rechazados = adapter.obtener_usuarios_invitados_evento(evento_id,Asistencia.NoAsisto)

        current_app.logger.info('Obteniendo usuarios invitados...')
        usuarios_invitados = usuarios_confirmados+usuarios_pendientes+usuarios_rechazados

        current_app.logger.info('Obteniendo usuarios para invitar...')
        users_to_invite = [user for user in all_users if user not in usuarios_invitados]
        requerimientos = adapter.obtener_requerimientos_evento(evento_id)

        current_app.logger.info('Obteniendo requerimientos con datos...')
        requerimientos_con_datos = []
        for r in requerimientos:
            asignaciones = adapter.obtener_asignaciones_requerimiento(r.id)
            faltan_reservar = r.cantidad
            asignacion_propia = {"cantidad":1}
            for a in asignaciones:
                faltan_reservar = faltan_reservar - a["cantidad"]
                if a["usuario_id"]==current_user.id:
                    asignacion_propia = a
                    faltan_reservar = faltan_reservar + a["cantidad"]

            requerimientos_con_datos.append({"requerimiento":r,"faltan_reservar":faltan_reservar,"asignacion_propia":asignacion_propia})

        headers = {'Content-Type': 'text/html'}
    	return make_response(render_template('evento.html',Asistencias=Asistencia,asistencia_actual=asistencia_actual.value,puede_editar=puede_editar,evento=evento,all_users=users_to_invite,usuarios_rechazados=usuarios_rechazados,usuarios_confirmados=usuarios_confirmados,usuarios_pendientes=usuarios_pendientes, clima_actual=clima_actual, requerimientos_con_datos=requerimientos_con_datos),200,headers)

    @login_required    
    def post(self,evento_id): 
        invitado_id = request.form['invitado']
        adapter.crear_invitacion(evento_id,invitado_id)
        current_app.logger.info('El usuario '+ invitado_id + ' fue invitado con exito al evento ' + evento_id)
        return {'invitado': invitado_id}

    def doSomething():
        current_app.logger.info('doSomething')
