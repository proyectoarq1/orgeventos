from mongo_models import User, session, Evento
from adapter import Adapter

from alchemy_encoder import MongoAlchemyEncoder
import dbsettings
from pymongo import MongoClient
import json, os
from bson.objectid import ObjectId
from datetime import date

from flask import current_app

from evento_form import EventoForm

class MongoAdapter(Adapter):

	session=session
	encoder = MongoAlchemyEncoder

	def crear_usuario(self, usuario_nombre):
		usuario = {"nombre":usuario_nombre}
		self.db.usuarios.insert_one(usuario)
		return usuario

	def to_json(self, db_object):# casi cambiar todo?
		return json.loads(json.dumps(db_object, cls=self.encoder))

	def get_id(self, objecto):#
		return objecto.mongo_id

	def guardar(self,objeto):
		self.session.save(objeto)

	def borrar(self,objeto):
		self.session.remove(objeto)

	def create_user(self, user_username, user_password, user_email):# cambiar por guardar?
		user = User(username=user_username, password=user_password , email=user_email)
	  	self.guardar(user)
	  	return user

	def get_user_by_id(self,user_id):
		user = self.session.query(User).filter_by(mongo_id=user_id).first()
		print user
		return user


	def get_userJson_by_id(self,user_id):# cambiar por get_user_by_id
		user = self.get_user_by_id(user_id) 
		return self.to_json(user)

	def get_usuario(self,usuario_id):
		pass
	#	usuario = self.session.query(Usuario).filter_by(id=usuario_id).first()
	#	return self.to_json(usuario)

	def get_usuarios(self):# cambiar por get users
		usuarios = []
		usuarios_base = Users.query.all()
		for u in usuarios_base:
		  usuarios.append(self.to_json(u))
		return usuarios

	def borrar_usuario(self,usuario_id): #cambir por buscar usuario y usar borrar
		db_session = self.session
		usuario = self.get_user_by_id(user_id)
		eventos_usuario = db_session.query(Evento).filter_by(organizador_id=usuario_id).all()
		for e in eventos_usuario:
			#db_session.delete(e)
			self.borrar(e)
		#db_session.delete(usuario)
		self.borrar(usuario)	
		#db_session.commit()	

	def crear_evento(self, usuario_id, form):
		db_session = self.session
		usuario = self.get_userJson_by_id(usuario_id)
		print usuario
		evento = Evento(organizador=usuario["username"],
						organizador_id=usuario_id,
						nombre=form.nombre.data,
						fecha=form.fecha.data,
						descripcion=form.descripcion.data,
						asistiran=0)
		self.guardar(evento)
		#db_session.add(evento)
		#db_session.commit()
		return evento

	def get_evento(self,user_id,evento_id):
		evento = self.session.query(Evento).filter_by(mongo_id=evento_id).first()
		return self.to_json(evento)

 	def obtener_eventos_asignados(self, usuario_id):#
		eventos_usuario = self.session.query(Evento).filter_by(organizador_id=usuario_id).all()
		eventos = []
		for e in eventos_usuario:
		  eventos.append(self.to_json(e))
		return eventos

	#def obtener_eventos_asignados2(self, user_id):
	#	eventos_usuario = self.session.query(Evento).filter_by(organizador_id=user_id).all()
	#	eventos = []
	#	for e in eventos_usuario:
	#	  eventos.append(self.to_json(e))
	#	return eventos

	def borrar_evento(self,user_id,evento_id):
		db_session = self.session
		evento = db_session.query(Evento).filter_by(mongo_id=evento_id).first()
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
			lista_invitaciones.append(e.mongo_id)
		return lista_invitaciones

	def borrar_invitacion(self, evento_id, usuario_id):
		evento = self.session.query(Evento).filter_by(mongo_id=evento_id).first()
		evento.invitados.remove(usuario_id)
		self.guardar(evento)



if __name__ == '__main__':

	#adapter = Adapter()

	adapter = MongoAdapter()
	usuario = adapter.create_user("user_username", "user_password", "user_email")
	print usuario
	usuario_id = adapter.get_id(usuario)
	print usuario_id

	#evento = adapter.crear_evento(usuario["_id"],None)
	#evento = adapter.crear_evento(usuario["_id"],None)
	#print evento

	form_evento1 = EventoForm(nombre="Evento uno", fecha=None, descripcion="Me gustaria poder organizar una juntada")
	form_evento2 = EventoForm(nombre="Evento dos", fecha=None, descripcion="Hagamos tambien otra juntada mas")
	print session.query(User).filter_by(mongo_id=usuario_id).first()
	
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
	print "Usuarios invitados"
	usuarios_invitados = adapter.obtener_usuarios_invitados_evento(evento_id1)
	print usuarios_invitados
	print usuario_id
	adapter.borrar_invitacion(evento_id1,usuario_id)
	invitaciones = adapter.obtener_invitaciones_usuario(usuario_id)
	print invitaciones
	print evento_id1
	usuarios_invitados = adapter.obtener_usuarios_invitados_evento(evento_id1)
	print usuarios_invitados
	print usuario_id
	

