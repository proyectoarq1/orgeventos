from models import Usuario, Session, Evento
from alchemy_encoder import AlchemyEncoder
import dbsettings
from pymongo import MongoClient
import json, os
from bson.objectid import ObjectId

class Adapter():

	def get_usuario(self,usuario_id):
		pass

	def obtener_eventos_asignados(self, usuario_id):
		pass

	def get_evento(self,user_id,evento_id):
		pass

	def crear_evento(self, usuario_id, form):
		pass

	def get_id(self, objecto):
		pass


class MongoDBAdapter(Adapter):

	#mongod --config c:\mongodb\mongo.config
	


	url = dbsettings.MONGO_DATABASE["url_conection"]
	client = MongoClient(url)
	db = client['prueba']

	def get_id(self, objecto):
		return objecto["_id"]

	def get_usuario(self,usuario_id):
		usuario = self.db.usuarios.find_one({"_id": ObjectId(usuario_id)})
		return usuario
		

	def obtener_eventos_asignados(self, usuario_id):
		usuario = self.get_usuario(usuario_id)
		return usuario["eventos"]

	def get_evento(self,user_id,evento_id):
		evento = self.db.eventos.find_one({"_id": ObjectId(evento_id)})
		return evento

	def crear_usuario(self, usuario_nombre):
		usuario = {"nombre":usuario_nombre}
		self.db.usuarios.insert_one(usuario)
		return usuario

	def crear_evento(self, usuario_id, form):
		usuario = self.get_usuario(usuario_id)
		evento = {"organizador":usuario["nombre"],
				  "organizador_id":usuario["_id"],
				  "nombre":form.nombre.data,
				  "fecha":form.fecha.data,
				  "descripcion":form.descripcion.data,
				  "asistiran":0}
		self.db.eventos.insert_one(evento)
		self.db.usuarios.update({"_id": ObjectId(usuario_id)},{'$push': {'eventos': evento}})
		return evento


class MySQLAdapter(Adapter):

	def get_id(self, objecto):
		return objecto.id

	def to_json(self, db_object):
		return json.loads(json.dumps(db_object, cls=AlchemyEncoder))

 	def obtener_eventos_asignados(self, usuario_id):
		eventos_usuario = Session().query(Evento).filter_by(organizador_id=usuario_id).all()
		eventos = []
		for e in eventos_usuario:
		  eventos.append(self.to_json(e))
		return eventos

	def crear_usuario(self, usuario_nombre):
		db_session = Session()
		usuario = Usuario(nombre=usuario_nombre)
		db_session.add(usuario)
		db_session.commit()
		return usuario

	def get_usuario(self,usuario_id):
		usuario = Session().query(Usuario).filter_by(id=usuario_id).first()
		return self.to_json(usuario)

	def get_evento(self,user_id,evento_id):
		evento = Session().query(Evento).filter_by(id=evento_id).first()
		return self.to_json(evento)

	def crear_evento(self, usuario_id, form):
		db_session = Session()
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

db_seleccionada = os.getenv('DATABASE_TO_USE', 'MySQL')

if db_seleccionada=='MySQL':
	adapter = MongoDBAdapter()
else:
	adapter = MongoDBAdapter()

if __name__ == '__main__':

	adapter = MongoDBAdapter()
	usuario = adapter.crear_usuario("Juan")
	print usuario

	evento = adapter.crear_evento(usuario["_id"],None)
	evento = adapter.crear_evento(usuario["_id"],None)
	print evento
	print "----------"
	print "----------"
	print "----------"
	print adapter.get_usuario(usuario["_id"])
