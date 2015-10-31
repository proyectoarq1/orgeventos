from flask import Flask, render_template, make_response, redirect, url_for, current_app
from flask_restful import Resource
from db.adapter_selected import adapter
from flask import session,request
from flask.ext.login import current_user
import urllib2, json


def get_clima(nombre_ciudad):

    url = "http://api.openweathermap.org/data/2.5/weather?q="+nombre_ciudad+"&units=metric"+"&appid=713d008f823124ef813cfef342341934"

    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    resultado = json.loads(response.read())
    clima = {
        'ubicacion': nombre_ciudad,
        'cielo': resultado["weather"][0]["main"],
        'descripcion': resultado["weather"][0]["description"],
        'temperatura': resultado["main"]["temp"],
        'icono' : resultado["weather"][0]["icon"]
    }
    return clima

class EventoController(Resource):
    def get(self,evento_id):
        evento = adapter.get_evento(evento_id)
        clima_actual = get_clima(evento["ubicacion"])
        all_users = adapter.get_all_users()
        headers = {'Content-Type': 'text/html'}
        usuarios_invitados = adapter.obtener_usuarios_invitados_evento(evento_id)
    	current_app.logger.info('invitados')
    	return make_response(render_template('evento.html',evento=evento,all_users=all_users,usuarios_invitados=usuarios_invitados, clima_actual=clima_actual),200,headers)

    def post(self,evento_id):        
        current_app.logger.info('Agregando un invitado')
        invitado_id = request.form['invitado']
        adapter.crear_invitacion(evento_id,invitado_id)
        #
        headers = {'Content-Type': 'text/html'}
        return redirect(url_for('evento', evento_id=evento_id))

    def doSomething():
        current_app.logger.info('doSomething')
