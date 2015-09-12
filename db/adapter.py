from models import Usuario, Session, Evento
from alchemy_encoder import AlchemyEncoder
import dbsettings
from pymongo import MongoClient
import json, os

class Adapter():

	def get_usuario(self,usuario_id):
		pass

	def obtener_eventos_asignados(self, usuario_id):
		pass

	def get_evento(self,user_id,evento_id):
		pass

	def crear_evento(self, usuario_id, form):
		pass


class MongoDBAdapter(Adapter):

	#mongod --config c:\mongodb\mongo.config
	
	url = dbsettings.MONGO_DATABASE["url_conection"]
	client = MongoClient(url)
	db = client['prueba']

	def get_usuario(self,usuario_id):
		usuario = db.usuarios.find_one({"id": usuario_id})
		return usuario
		

	def obtener_eventos_asignados(self, usuario_id):
		usuario = db.usuarios.find_one({"_id": usuario_id})
		return usuario["eventos"]

	def get_evento(self,user_id,evento_id):
		evento = db.eventos.find_one({"_id": evento_id})
		return evento

	def crear_usuario(self, usuario_nombre):
		usuario = self.get_usuario(usuario_id)
		evento = {"nombre":usuario_nombre}
		db.usuarios.insert_one(evento)

	def crear_evento(self, usuario_id, form):
		usuario = self.get_usuario(usuario_id)
		evento = {"organizador":usuario["nombre"],
				  "organizador_id":usuario.id,
				  "nombre":form.nombre.data,
				  "fecha":form.fecha.data,
				  "descripcion":form.descripcion.data,
				  "asistiran":0}
		#db.eventos.insert_one(evento).inserted_id
		db.usuarios.update({"_id": usuario_id},{'$push': {'eventos': {evento}}})


class MySQLAdapter(Adapter):

	def to_json(self, db_object):
		return json.loads(json.dumps(db_object, cls=AlchemyEncoder))

 	def obtener_eventos_asignados(self, usuario_id):
		eventos_usuario = Session().query(Evento).filter_by(organizador_id=usuario_id).all()
		eventos = []
		for e in eventos_usuario:
		  eventos.append(self.to_json(e))
		return eventos

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

db_seleccionada = os.getenv('DATABASE_TO_USE', 'MySQL')

if db_seleccionada=='MySQL':
	adapter = MySQLAdapter()
else:
	adapter = MongoDBAdapter()

if __name__ == '__main__':

	if 1==0:
		url = dbsettings.MONGO_DATABASE["url_conection"]
		client = MongoClient(url)
		db = client['prueba']
		post = {"author": "Mike", "hola":[]}
		posts = db.posts
		post_id = posts.insert_one(post).inserted_id
		a=posts.find_one({"_id": post_id})
		print a
		posts.update({"_id": post_id},{'$push': {'hola': {'name': 'item5'}}})
		posts.update({"_id": post_id},{'$push': {'hola': {'name': 'item333','name': 'item33'}}})
		a=posts.find_one({"_id": post_id})
		print a["hola"]
		print type(a)


	usuario = Session().query(Usuario).first()

	pa= json.loads(json.dumps(usuario, cls=AlchemyEncoder))

	print pa
	print pa["nombre"]
	print type(pa)

