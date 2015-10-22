from models import Usuario, User, Session, Evento, Invitacion
import datetime
from alchemy_encoder import AlchemyEncoder
import dbsettings
from pymongo import MongoClient
import json, os
from bson.objectid import ObjectId
from datetime import date
from abc import ABCMeta, abstractmethod

from flask import current_app

#from evento_form import EventoForm

class Adapter():

	__metaclass__ = ABCMeta

	@abstractmethod
	def get_id(self, objecto):
		pass

	@abstractmethod
	def crear_usuario(self, usuario_nombre):
		pass

	@abstractmethod
	def get_usuario(self,usuario_id):
		pass

	@abstractmethod
	def get_user_by_id(self,user_id):
		pass

	def get_usuarios(self):
		pass

	@abstractmethod
	def borrar_usuario(self,usuario_id):
		pass

	@abstractmethod
	def crear_evento(self, usuario_id, form):
		pass

	@abstractmethod
	def get_evento(self,user_id,evento_id):
		pass

	@abstractmethod
	def obtener_eventos_asignados(self, usuario_id):
		pass

	@abstractmethod
	def borrar_evento(self,user_id,evento_id):
		pass

	@abstractmethod
	def crear_invitacion(self, evento_id, usuario_id):
		pass

	@abstractmethod
	def obtener_usuarios_invitados_evento(self, evento_id):
		pass

	@abstractmethod
	def obtener_invitaciones_usuario(self, usuario_id):
		pass

	@abstractmethod
	def borrar_invitacion(self, evento_id, usuario_id):
		pass

class MongoDBAdapter(Adapter):

	#mongod --config c:\mongodb\mongo.config
	def __init__():
		url = dbsettings.MONGO_DATABASE["url_conection"]
		client = MongoClient(url)
		db = client['prueba']

	def get_id(self, objecto):
		return str(objecto["_id"])

	def crear_usuario(self, usuario_nombre):
		usuario = {"nombre":usuario_nombre}
		self.db.usuarios.insert_one(usuario)
		return usuario

	def get_usuario(self,usuario_id):
		usuario = self.db.usuarios.find_one({"_id": ObjectId(usuario_id)})
		return usuario
	
	def get_user_by_id(self,user_id):
		user = self.db.user.find_one({"_id": ObjectId(user_id)})
		return user

	def get_usuarios(self):
		return self.db.usuarios.find()
	
	def borrar_usuario(self,usuario_id):
		self.db.usuarios.remove({"_id": ObjectId(usuario_id)})
		self.db.eventos.remove({'organizador_id': ObjectId(usuario_id)})

	def crear_evento(self, usuario_id, form):
		usuario = self.get_usuario(usuario_id)
		evento = {"organizador":usuario["nombre"],
				  "organizador_id":usuario["_id"],
				  "nombre": form.nombre.data,
				  "fecha": str(form.fecha.data),
				  "descripcion": form.descripcion.data,
				  "asistiran":0}
		self.db.eventos.insert_one(evento)
		self.db.usuarios.update({"_id": ObjectId(usuario_id)},{'$push': {'eventos': evento}})
		return evento

	def get_evento(self,usuario_id,evento_id):
		evento = self.db.eventos.find_one({"_id": ObjectId(evento_id)})
		return evento

	def obtener_eventos_asignados(self, usuario_id):
		usuario = self.get_usuario(usuario_id)
		eventos = []
		if "eventos" in usuario:
			eventos = usuario["eventos"]
		return eventos

	def borrar_evento(self,usuario_id,evento_id):
		self.db.eventos.remove({"_id":ObjectId(evento_id)})
		self.db.usuarios.update({"_id": ObjectId(usuario_id)}, { '$unset' : { 'eventos' : {'_id':ObjectId(evento_id)} }})

	def crear_invitacion(self, evento_id, usuario_id):
		self.db.eventos.update({"_id": ObjectId(evento_id)},{'$push': {'invitados': usuario_id}})
		self.db.usuarios.update({"_id": ObjectId(usuario_id)},{'$push': {'invitaciones': evento_id}})

	def obtener_usuarios_invitados_evento(self, evento_id):
		evento = self.get_evento(None,evento_id)
		invitados = []
		if "invitados" in evento:
			invitados = evento["invitados"]
		return invitados	

	def obtener_invitaciones_usuario(self, usuario_id):
		usuario = self.get_usuario(usuario_id)
		invitaciones = []
		if "invitaciones" in usuario:
			invitaciones = usuario["invitaciones"]
		return invitaciones
		
	def borrar_invitacion(self, evento_id, usuario_id):
		self.db.usuarios.update({"_id": ObjectId(usuario_id)}, { '$unset' : { 'invitaciones' : {'_id':ObjectId(evento_id)} }})
		self.db.eventos.update({"_id": ObjectId(evento_id)}, { '$unset' : { 'invitados' : {'_id':ObjectId(usuario_id)} }})


class MySQLAdapter(Adapter):

	session=Session()

	def to_json(self, db_object):
		return json.loads(json.dumps(db_object, cls=AlchemyEncoder))

	def get_id(self, objecto):
		return objecto.id

	def crear_usuario(self, usuario_nombre):
		db_session = self.session
		usuario = Usuario(nombre=usuario_nombre)
		db_session.add(usuario)
		db_session.commit()
		return usuario

	def create_user(self, user_username, user_password, user_email):
		db_session = self.session
		user = User(username=user_username, password=user_password , email=user_email)
		current_app.logger.info('create_user  ')
	  	db_session.add(user)
	  	db_session.commit()
	  	return user

	def get_user_by_id(self,user_id):
		return self.session.query(User).filter_by(id=user_id).first() 

	def get_userJson_by_id(self,user_id):
		user = self.session.query(User).filter_by(id=user_id).first() 
		return self.to_json(user)

	def get_usuario(self,usuario_id):
		usuario = self.session.query(Usuario).filter_by(id=usuario_id).first()
		return self.to_json(usuario)

	def get_usuarios(self):
		usuarios = []
		usuarios_sql = Usuario.query.all()
		for u in usuarios_sql:
		  usuarios.append(self.to_json(u))
		return usuarios

	def borrar_usuario(self,usuario_id):
		db_session = self.session
		usuario = db_session.query(Usuario).filter_by(id=usuario_id).first()
		eventos_usuario = db_session.query(Evento).filter_by(organizador_id=usuario_id).all()
		for e in eventos_usuario:
			db_session.delete(e)
		db_session.delete(usuario)		
		db_session.commit()	

	def crear_evento(self, usuario_id, form):
		db_session = self.session
		usuario = self.get_userJson_by_id(usuario_id)
		evento = Evento(organizador=usuario["username"],
						organizador_id=usuario_id,
						nombre=form.nombre.data,
						categoria=form.categoria.data,
						fecha=datetime.datetime.strptime(form.fecha.data + " " + form.hora.data, "%d/%m/%Y %H:%M"),
						descripcion=form.descripcion.data,
						ubicacion=form.ubicacion.data,
						asistiran=0)
		db_session.add(evento)
		db_session.commit()
		return evento

	def get_evento(self,user_id,evento_id):
		evento = self.session.query(Evento).filter_by(id=evento_id).first()
		return self.to_json(evento)

 	def obtener_eventos_asignados(self, usuario_id):
		eventos_usuario = self.session.query(Evento).filter_by(organizador_id=usuario_id, categoria="Privado").all()
		eventos = []
		for e in eventos_usuario:
		  eventos.append(self.to_json(e))
		return eventos

	def obtener_eventos_publicos(self):
		eventos_publicos = self.session.query(Evento).filter_by(categoria="Publico").all()
		eventos = []
		for e in eventos_publicos:
		  eventos.append(self.to_json(e))
		return eventos

	def obtener_eventos_asignados2(self, user_id):
		eventos_usuario = self.session.query(Evento).filter_by(organizador_id=user_id).all()
		eventos = []
		for e in eventos_usuario:
		  eventos.append(self.to_json(e))
		return eventos

	def borrar_evento(self,user_id,evento_id):
		db_session = self.session
		evento = db_session.query(Evento).filter_by(id=evento_id).first()
		db_session.delete(evento)
		db_session.commit()

	def crear_invitacion(self, evento_id, usuario_id):
		db_session = self.session
		invitacion = Invitacion(evento_id=evento_id, usuario_id=usuario_id)
		db_session.add(invitacion)
		db_session.commit()

	def obtener_usuarios_invitados_evento(self, evento_id):
		db_session = self.session
		invitaciones_evento = self.session.query(Invitacion).filter_by(evento_id=evento_id).all()
		usuarios_invitados = []
		for invitacion in invitaciones_evento:
			usuarios_invitados.append(invitacion.usuario_id)
		return usuarios_invitados

	def obtener_invitaciones_usuario(self, usuario_id):
		db_session = self.session
		invitaciones_usuario = self.session.query(Invitacion).filter_by(usuario_id=usuario_id).all()
		lista_invitaciones = []
		for invitacion in invitaciones_usuario:
			lista_invitaciones.append(invitacion.evento_id)
		return lista_invitaciones

	def borrar_invitacion(self, evento_id, usuario_id):
		db_session = self.session
		invitacion = self.session.query(Invitacion).filter_by(evento_id=evento_id, usuario_id=usuario_id).first()
		db_session.delete(invitacion)
		db_session.commit()





db_seleccionada = os.getenv('TIPO_BASE_DE_DATOS', 'MySQL')

if db_seleccionada=='MongoDB':
	adapter = MongoDBAdapter()
else:
	adapter = MySQLAdapter()

if __name__ == '__main__':

	#adapter = Adapter()

	adapter = MySQLAdapter()
	usuario = adapter.crear_usuario("Juan")
	print usuario
	usuario_id = adapter.get_id(usuario)

	#evento = adapter.crear_evento(usuario["_id"],None)
	#evento = adapter.crear_evento(usuario["_id"],None)
	#print evento

#	form_evento1 = EventoForm(nombre="Evento uno", fecha=None, descripcion="Me gustaria poder organizar una juntada")
#	form_evento2 = EventoForm(nombre="Evento dos", fecha=None, descripcion="Hagamos tambien otra juntada mas")

	
	e1 = adapter.crear_evento(usuario_id,None)#form_evento1)
	evento_id1 = adapter.get_id(e1)
	e2 = adapter.crear_evento(usuario_id,None)#form_evento2)
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
	

