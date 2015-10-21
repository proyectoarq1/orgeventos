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
import mongoAdapter

#from evento_form import EventoForm

class Adapter():

	__metaclass__ = ABCMeta

	@abstractmethod
	def to_json(self, db_object):
		pass

	@abstractmethod
	def get_id(self, objecto):
		pass

	def create_user(self, user_username, user_password, user_email):# ESTE VA PARA ARRIBA
		user = User(username=user_username, password=user_password , email=user_email)
	  	self.guardar(user)
	  	return user

	@abstractmethod
	def get_user_by_id(self,user_id):
		pass

	def get_userJson_by_id(self,user_id):
		user = self.get_user_by_id(user_id) 
		return self.to_json(user)

	def get_usuarios(self):
		usuarios = []
		usuarios_sql = Usuario.query.all()
		for u in usuarios_sql:
		  usuarios.append(self.to_json(u))
		return usuarios

	def borrar_usuario(self,usuario_id):
		usuario = self.get_user_by_id(user_id)
		eventos_usuario = self.db_session.query(Evento).filter_by(organizador_id=usuario_id).all()
		for e in eventos_usuario:
			self.borrar(e)
		self.borrar(usuario)

	def crear_evento(self, usuario_id, form):
		usuario = self.get_userJson_by_id(usuario_id)
		evento = Evento(organizador=usuario["username"],
						organizador_id=usuario_id,
						nombre=form.nombre.data,
						fecha=datetime.datetime.strptime(form.fecha.data + " " + form.hora.data, "%d/%m/%Y %H:%M"),
						descripcion=form.descripcion.data,
						ubicacion=form.ubicacion.data,
						asistiran=0)
		self.guardar(evento)
		return evento

	@abstractmethod
	def get_evento(self,evento_id):
		pass

	def obtener_eventos_asignados(self, usuario_id):
		eventos_usuario = self.db_session.query(Evento).filter_by(organizador_id=usuario_id).all()
		eventos = []
		for e in eventos_usuario:
		  eventos.append(self.to_json(e))
		return eventos

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


if __name__ == '__main__':

	pass

