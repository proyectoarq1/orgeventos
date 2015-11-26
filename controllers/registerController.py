from flask import Flask, render_template, flash, request, redirect, url_for, session, make_response, current_app
from flask_restful import Resource
from db.adapter_selected import adapter
from formularios.usuario_form import UserForm
from flask.ext.mail import Message, Mail
import os


class RegisterController(Resource):
	def get(self):
		form = UserForm(request.form)
		headers = {'Content-Type': 'text/html'}
		return make_response(render_template('register.html', form=form, editar=False),200,headers)

	def post(self):
		form = UserForm(request.form)
		if form.validate():
			user = adapter.create_user(form)
			current_app.logger.info('El usuario se creo con exito')
			#
			mail = Mail()
			mail.init_app(current_app)
			msg = Message("Arreglamos Eh", sender="arqsoft12015@gmail.com", recipients=[user.email])
			msg.html = "<b>Felicitaciones!!, Te has logueado satisfactoriamente</b>"
			mail.send(msg)
			#
			return redirect(url_for('login'))
		else:
			current_app.logger.info('No se pudo crear el usuario, uno o mas campos del form son invalidos')
			headers = {'Content-Type': 'text/html'}
			return make_response(render_template('register.html', form=form, editar=False),200,headers)