from models import Usuario, Session, Evento


class Adapter():

	def get_usuario(self,usuario_id):
		pass

	def obtener_eventos_asignados(self, usuario_id):
		pass

	def get_evento(self,evento_id):
		pass


class MongoDBAdapter(Adapter):
	pass

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
