from mongo_models import User, session, Evento
from adapter import Adapter

from alchemy_encoder import MongoAlchemyEncoder
import dbsettings
from pymongo import MongoClient
import json, os
from bson.objectid import ObjectId
from datetime import date, datetime

from flask import current_app

from evento_form import EventoForm

class MongoAdapter(Adapter):

	session=session
	encoder = MongoAlchemyEncoder

	def to_json(self, db_object):
		return json.loads(json.dumps(db_object, cls=self.encoder))

	def get_id(self, objecto):
		return objecto.mongo_id

	def guardar(self,objeto):
		self.session.save(objeto)

	def borrar(self,objeto):
		self.session.remove(objeto)

	def get_user_by_id(self,user_id):
		user = self.session.query(User).filter_by(mongo_id=user_id).first()
		return user	

	def get_evento(self,evento_id):
		evento = self.session.query(Evento).filter_by(mongo_id=evento_id).first()
		return self.to_json(evento)

	def borrar_evento(self,user_id,evento_id):
		evento = self.session.query(Evento).filter_by(mongo_id=evento_id).first()
		self.borrar(evento)

	def crear_invitacion(self, evento_id, usuario_id):
		evento = self.session.query(Evento).filter_by(mongo_id=evento_id).first()
		evento.invitados.append(usuario_id)
		self.guardar(evento)

	def obtener_usuarios_invitados_evento(self, evento_id):
		evento = self.get_evento(evento_id)
		return evento["invitados"]

	def obtener_invitaciones_usuario(self, usuario_id):
		eventos = self.session.query(Evento).filter({ "invitados": [ usuario_id ] }).all()
		lista_invitaciones = []
		for e in eventos:
			lista_invitaciones.append(str(e.mongo_id))
		return lista_invitaciones

	def borrar_invitacion(self, evento_id, usuario_id):
		evento = self.session.query(Evento).filter_by(mongo_id=evento_id).first()
		evento.invitados.remove(usuario_id)
		self.guardar(evento)



if __name__ == '__main__':

	#adapter = Adapter()
	session.clear_collection(User)
	adapter = MongoAdapter()
	usuario = adapter.create_user("user_username11", "user_password888", "user_email11")
	print usuario
	usuario_id = adapter.get_id(usuario)
	print "usuario id"
	print usuario_id
	print "el usuario q deberia traer"
	print adapter.get_user_by_id(usuario_id)
	print adapter.get_userJson_by_id(usuario_id)
	#evento = adapter.crear_evento(usuario["_id"],None)
	#evento = adapter.crear_evento(usuario["_id"],None)
	#print evento

	if (True):
		form_evento1 = EventoForm(nombre="Evento uno", fecha=None, descripcion="Me gustaria poder organizar una juntada")
		form_evento2 = EventoForm(nombre="Evento dos", fecha=None, descripcion="Hagamos tambien otra juntada mas")
		
		
		e1 = adapter.crear_evento(usuario_id,form_evento1)
		evento_id1 = adapter.get_id(e1)
		e2 = adapter.crear_evento(usuario_id,form_evento2)
		evento_id2 = adapter.get_id(e2)
		

		adapter.crear_invitacion(evento_id1,usuario_id)
		adapter.crear_invitacion(evento_id2,usuario_id)
		invitaciones = adapter.obtener_invitaciones_usuario(usuario_id)
		print "invitaciones de usuarios"
		print invitaciones
		print evento_id1
		print "--------------------------------"
		print "Usuarios invitados"
		usuarios_invitados = adapter.obtener_usuarios_invitados_evento(evento_id1)
		print usuarios_invitados
		print usuario_id
		print "--------------------------------"
		
		adapter.borrar_invitacion(evento_id1,usuario_id)
		invitaciones = adapter.obtener_invitaciones_usuario(usuario_id)
		print "invitaciones de usuario cuando se borro el unico usuario_id"
		print invitaciones
		print evento_id1
		print "--------------------------------"
		usuarios_invitados = adapter.obtener_usuarios_invitados_evento(evento_id1)
		print "invitaciones de evento cuando se borro el unico usuario_id"
		print usuarios_invitados
		print usuario_id
		print "--------------------------------"
		usuarios_invitados = adapter.obtener_usuarios_invitados_evento(evento_id2)
		print "invitaciones de evento2 cuando se borro el unico usuario_id"
		print usuarios_invitados
		print usuario_id
		print "--------------------------------"

