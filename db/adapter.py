
import os

db_seleccionada = os.getenv('TIPO_BASE_DE_DATOS', 'MySQL')

if db_seleccionada=='MongoDB':
	from mongo_models import User, Evento
else:
	from models import User, Evento, Requerimiento

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

	def create_user(self, form):# ESTE VA PARA ARRIBA
		user = User(username=form.username.data, 
					password=form.password.data , 
					email=form.email.data)
	  	self.guardar(user)
	  	return user

	def guardar_edicion_a_usuario(self, usuario_id, form):
		usuario = self.get_user_by_id(usuario_id)
	
		usuario.username = form.username.data
		usuario.password=form.password.data
		usuario.email=form.email.data
			
		self.guardar(usuario)
		return usuario

	def get_user_by_name_and_pass(self,username, password):
		registered_user = self.db_session.query(User).filter_by(username=username,password=password).first()
		return registered_user

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

	@abstractmethod
	def get_all_users(self):
		pass

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
						categoria=form.categoria.data,
						fecha=datetime.datetime.strptime(form.fecha.data, "%d/%m/%Y"),
						hora= form.hora.data,
						descripcion=form.descripcion.data,
						ubicacion=form.ubicacion.data,
						url_imagen=form.url_imagen.data,
						asistiran=0)
		
		self.guardar(evento)
		self.crear_invitacion(evento.id, usuario_id)
		self.confirmar_asistencia_a_evento(evento.id, usuario_id)
		return evento

	@abstractmethod
	def get_evento_object(self,evento_id):
		pass

	def guardar_edicion_a_evento(self, evento_id, form):
		evento = self.get_evento_object(evento_id)
		
		evento.nombre = form.nombre.data
		evento.categoria=form.categoria.data
		evento.fecha=datetime.datetime.strptime(form.fecha.data, "%d/%m/%Y")
		evento.hora= form.hora.data
		evento.descripcion=form.descripcion.data
		evento.ubicacion=form.ubicacion.data
		evento.url_imagen=form.url_imagen.data
		
		self.guardar(evento)
		return evento


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

	@abstractmethod
	def get_evento(self,evento_id):
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
	def obtener_usuario_invitado_evento(self, evento_id, usuario_id):
		pass

	@abstractmethod
	def confirma_asistencia_a_evento(self, evento_id, usuario_id):
		pass

	@abstractmethod
	def confirmar_asistencia_a_evento(self, evento_id, usuario_id):
		pass

	@abstractmethod
	def obtener_eventos_invitados(self, usuario_id):
		pass

	@abstractmethod
	def rechazar_asistencia_a_evento(self, evento_id, usuario_id):
		pass

	@abstractmethod
	def obtener_invitaciones_usuario(self, usuario_id):
		pass

	@abstractmethod
	def borrar_invitacion(self, evento_id, usuario_id):
		pass

	def crear_requerimiento(self, evento_id, form):
		
		requerimiento = Requerimiento(
			nombre=form.nombre.data,
			descripccion=form.descripccion.data,
			cantidad=form.cantidad.data)
		
		self.guardar(requerimiento)
		
		return requerimiento

	@abstractmethod
	def borrar_requerimiento(self, requerimiento_id):
		pass

	@abstractmethod
	def obtener_requerimientos_evento(self, evento_id):
		pass



