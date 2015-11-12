from models import User, Session, Evento, Invitacion, Requerimiento
import datetime
from alchemy_encoder import AlchemyEncoder
import dbsettings
from pymongo import MongoClient
import json, os
from bson.objectid import ObjectId
from datetime import date
from abc import ABCMeta, abstractmethod

from flask import current_app
from adapter import Adapter

#from evento_form import EventoForm

class MySQLAdapter(Adapter):

	db_session=Session()
	db_session.rollback()

	def to_json(self, db_object):
		return json.loads(json.dumps(db_object, cls=AlchemyEncoder))

	def get_id(self, objecto):
		return objecto.id

	def guardar(self,objeto):
		self.db_session.add(objeto)
	  	self.db_session.commit()

	def borrar(self,objeto):
		self.db_session.delete(objeto)		
		self.db_session.commit()

	def get_user_by_id(self,user_id):
		return self.db_session.query(User).filter_by(id=user_id).first() 

	def get_all_users(self):
		return self.db_session.query(User).all() 

	def get_evento_object(self,evento_id):
		evento = self.db_session.query(Evento).filter_by(id=evento_id).first()
		return evento

	def get_evento(self,evento_id):
		evento = self.db_session.query(Evento).filter_by(id=evento_id).first()
		return self.to_json(evento)

	def obtener_eventos_asignados(self, usuario_id):
		eventos_usuario = self.db_session.query(Evento).filter_by(organizador_id=usuario_id, categoria="Privado").all()
		eventos = []
		for e in eventos_usuario:
		  eventos.append(self.to_json(e))
		return eventos

	def obtener_eventos_invitados(self, usuario_id):
		eventos_invitados = self.db_session.query(Invitacion).filter_by(usuario_id=usuario_id).all()
		eventos = []
		for e in eventos_invitados:
			evento = self.get_evento(e.evento_id)
			if str(evento['organizador_id']) != str(usuario_id):
				eventos.append(evento)
		return eventos

	def obtener_eventos_publicos(self):
		eventos_publicos = self.db_session.query(Evento).filter_by(categoria="Publico").all()
		eventos = []
		for e in eventos_publicos:
		  eventos.append(self.to_json(e))
		return eventos

	def borrar_evento(self,user_id,evento_id):
		evento = self.db_session.query(Evento).filter_by(id=evento_id).first()
		self.borrar(evento)

	def crear_invitacion(self, evento_id, usuario_id):
		invitacion = Invitacion(evento_id=evento_id, usuario_id=usuario_id)
		self.guardar(invitacion)

	def obtener_usuarios_invitados_evento(self, evento_id):
		db_session = self.db_session
		invitaciones_evento = self.db_session.query(Invitacion).filter_by(evento_id=evento_id).all()
		usuarios_invitados = []
		for invitacion in invitaciones_evento:
			usuarios_invitados.append(invitacion.usuario_id)
		usuarios = db_session.query(User).filter(User.id.in_(usuarios_invitados)).all()
		return usuarios

	def obtener_usuario_invitado_evento(self, evento_id, usuario_id):
		db_session = self.db_session
		usuario_invitado = self.db_session.query(Invitacion).filter_by(evento_id=evento_id, usuario_id=usuario_id).first()
		return get_user_by_id(usuario_invitado)

	def confirma_asistencia_a_evento(self, evento_id, usuario_id):
		db_session = self.db_session
		invitacion = self.db_session.query(Invitacion).filter_by(evento_id=evento_id, usuario_id=usuario_id).first()
		if invitacion:
			return invitacion.asiste
		else: 
			return False

	def confirmar_asistencia_a_evento(self, evento_id, usuario_id):
		db_session = self.db_session
		invitacion = self.db_session.query(Invitacion).filter_by(evento_id=evento_id, usuario_id=usuario_id).first()
		invitacion.asiste = True
		print invitacion
		self.guardar(invitacion)

	def rechazar_asistencia_a_evento(self, evento_id, usuario_id):
		db_session = self.db_session
		invitacion = self.db_session.query(Invitacion).filter_by(evento_id=evento_id, usuario_id=usuario_id).first()
		invitacion.asiste = False
		guardar(invitacion)

	def obtener_invitaciones_usuario(self, usuario_id):
		invitaciones_usuario = self.db_session.query(Invitacion).filter_by(usuario_id=usuario_id).all()
		lista_invitaciones = []
		for invitacion in invitaciones_usuario:
			lista_invitaciones.append(invitacion.evento_id)
		return lista_invitaciones

	def borrar_invitacion(self, evento_id, usuario_id):
		invitacion = self.db_session.query(Invitacion).filter_by(evento_id=evento_id, usuario_id=usuario_id).first()
		self.borrar(invitacion)

	def borrar_requerimiento(self, requerimiento_id):
		requerimiento = self.db_session.query(Requerimiento).filter_by(id=requerimiento_id).first()
		#Tambien hay que borrar todos los requerimientos asignados!!!
		requerimientos_asignados = self.db_session.query(RequerimientoAsignado).filter_by(requerimiento_id=requerimiento_id).all()
		for r in requerimientos_asignados:
			self.borrar(r)
		self.borrar(requerimiento)

	def obtener_requerimientos_evento(self, evento_id):
		requerimientos = self.db_session.query(Requerimiento).filter_by(evento_id=evento_id).all()
		requerimientos_json = []
		for r in requerimientos:
		  requerimientos_json.append(self.to_json(r))
		return requerimientos_json




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
	