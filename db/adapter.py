from models import Usuario, User, Session, Evento
from alchemy_encoder import AlchemyEncoder
import dbsettings
from pymongo import MongoClient
import json, os
from bson.objectid import ObjectId
from datetime import date
from abc import ABCMeta, abstractmethod
from flask import current_app

class Adapter():

	__metaclass__ = ABCMeta

	@abstractmethod
	def crear_usuario(self, usuario_nombre):
		pass

	@abstractmethod
	def get_usuario(self,usuario_id):
		pass

	@abstractmethod
	def get_user_by_id(self,user_id):
		pass

	@abstractmethod
	def borrar_usuario(self,usuario_id):
		pass

	@abstractmethod
	def obtener_eventos_asignados(self, usuario_id):
		pass

	@abstractmethod
	def get_evento(self,user_id,evento_id):
		pass

	@abstractmethod
	def borrar_evento(self,user_id,evento_id):
		pass

	@abstractmethod
	def crear_evento(self, usuario_id, form):
		pass

	@abstractmethod
	def get_id(self, objecto):
		pass


class MongoDBAdapter(Adapter):

	#mongod --config c:\mongodb\mongo.config
	


	url = dbsettings.MONGO_DATABASE["url_conection"]
	client = MongoClient(url)
	db = client['prueba']

	def get_id(self, objecto):
		return str(objecto["_id"])

	def get_usuario(self,usuario_id):
		usuario = self.db.usuarios.find_one({"_id": ObjectId(usuario_id)})
		return usuario

	def get_user_by_id(self,user_id):
		user = self.db.user.find_one({"_id": ObjectId(user_id)})
		return user
	
	def borrar_usuario(self,usuario_id):
		self.db.usuarios.remove({"_id": ObjectId(usuario_id)})
		self.db.eventos.remove({'organizador_id': ObjectId(usuario_id)})


	def obtener_eventos_asignados(self, usuario_id):
		usuario = self.get_usuario(usuario_id)
		return usuario["eventos"]

	def get_evento(self,usuario_id,evento_id):
		evento = self.db.eventos.find_one({"_id": ObjectId(evento_id)})
		return evento

	def borrar_evento(self,usuario_id,evento_id):
		self.db.eventos.remove({"_id":ObjectId(evento_id)})
		self.db.usuarios.update({"_id": ObjectId(usuario_id)}, { '$unset' : { 'eventos' : {'_id':ObjectId(evento_id)} }}) 	

	def crear_usuario(self, usuario_nombre):
		usuario = {"nombre":usuario_nombre}
		self.db.usuarios.insert_one(usuario)
		return usuario

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


class MySQLAdapter(Adapter):

	session=Session()

	def get_id(self, objecto):
		return objecto.id

	def to_json(self, db_object):
		return json.loads(json.dumps(db_object, cls=AlchemyEncoder))

	def borrar_usuario(self,usuario_id):
		db_session = self.session
		usuario = db_session.query(Usuario).filter_by(id=usuario_id).first()
		eventos_usuario = db_session.query(Evento).filter_by(organizador_id=usuario_id).all()
		for e in eventos_usuario:
			db_session.delete(e)
		db_session.delete(usuario)		
		db_session.commit()	

 	def obtener_eventos_asignados(self, usuario_id):
		eventos_usuario = self.session.query(Evento).filter_by(organizador_id=usuario_id).all()
		eventos = []
		for e in eventos_usuario:
		  eventos.append(self.to_json(e))
		return eventos

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

	def get_usuario(self,usuario_id):
		usuario = self.session.query(Usuario).filter_by(id=usuario_id).first()
		return self.to_json(usuario)

	def get_evento(self,user_id,evento_id):
		evento = self.session.query(Evento).filter_by(id=evento_id).first()
		return self.to_json(evento)

	def borrar_evento(self,user_id,evento_id):
		db_session = self.session
		evento = db_session.query(Evento).filter_by(id=evento_id).first()
		db_session.delete(evento)
		db_session.commit()

	def crear_evento(self, usuario_id, form):
		db_session = self.session
		usuario = self.get_usuario(usuario_id)
		evento = Evento(organizador=usuario["nombre"],
						organizador_id=usuario_id,
						nombre=form.nombre.data,
						fecha=form.fecha.data,
						descripcion=form.descripcion.data,
						asistiran=0)
		db_session.add(evento)
		db_session.commit()
		return evento

db_seleccionada = os.getenv('TIPO_BASE_DE_DATOS', 'MySQL')

if db_seleccionada=='MongoDB':
	adapter = MongoDBAdapter()
else:
	adapter = MySQLAdapter()

if __name__ == '__main__':

	#adapter = Adapter()

	adapter = MongoDBAdapter()
	usuario = adapter.crear_usuario("Juan")
	print usuario
	usuario_id = adapter.get_id(usuario)

	#evento = adapter.crear_evento(usuario["_id"],None)
	#evento = adapter.crear_evento(usuario["_id"],None)
	#print evento

	print "----------"
	print adapter.get_usuario(usuario_id)
	print "__________CON EVENTO Y USUARIO___________"
	e = adapter.crear_evento(usuario_id,None)
	evento_id = adapter.get_id(e)
	ee=adapter.get_evento(usuario_id,evento_id)
	print ee
	print "__________SIN EVENTO Y SIN USUARIO___________"
	#adapter.borrar_evento(usuario_id, evento_id)
	adapter.borrar_usuario(usuario_id)
	ee=adapter.get_evento(usuario_id,evento_id)
	u=adapter.get_usuario(usuario_id)
	print ee
	print u


