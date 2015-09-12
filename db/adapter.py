from models import Usuario, Session, Evento
import dbsettings
from pymongo import MongoClient

class Adapter():

	def get_usuario(self,usuario_id):
		pass

	def obtener_eventos_asignados(self, usuario_id):
		pass

	def get_evento(self,evento_id):
		pass

	def crear_evento(self, usuario_id, form):
		pass


class MongoDBAdapter(Adapter):
	
	url = dbsettings.MONGO_DATABASE["url_conection"]
	client = MongoClient(url)
	db = client['prueba']

	def get_usuario(self,usuario_id):
		
		usuario = db.usuarios.find_one({"id": usuario_id})
		return usuario
		

	def obtener_eventos_asignados(self, usuario_id):
		usuario = db.usuarios.find_one({"_id": usuario_id})
		return usuario["eventos"]

	def get_evento(self,evento_id):
		evento = db.eventos.find_one({"_id": evento_id})
		return evento

	def crear_evento(self, usuario_id, form):
		usuario = self.get_usuario(usuario_id)
		evento = {"organizador":usuario["nombre"],
				  "organizador_id":usuario.id,
				  "nombre":form.nombre.data,
				  "fecha":form.fecha.data,
				  "descripcion":form.descripcion.data,
				  "asistiran":0}
		db.eventos.insert_one(evento)
		db.usuarios.update({"_id": usuario_id},{'$push': {'eventos': {evento}}})


class MySQLAdapter(Adapter):

 	def obtener_eventos_asignados(self, usuario_id):
		eventos_usuario = Session().query(Evento).filter_by(organizador_id=usuario_id).all()
		eventos = []
		for e in eventos_usuario:
		  eventos.append(e)
		return eventos

	def get_usuario(self,usuario_id):
		usuario = Session().query(Usuario).filter_by(id=usuario_id).first()
		return usuario

	def get_evento(self,evento_id):
		evento = Session().query(Evento).filter_by(id=evento_id).first()
		return evento

	def crear_evento(self, usuario_id, form):
		db_session = Session()
		usuario = self.get_usuario(usuario_id)
		evento = Evento(organizador=usuario.nombre,
						organizador_id=usuario.id,
						nombre=form.nombre.data,
						fecha=form.fecha.data,
						descripcion=form.descripcion.data,
						asistiran=0)
		db_session.add(evento)
		db_session.commit()


adapter = MySQLAdapter()

if __name__ == '__main__':

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
	print a