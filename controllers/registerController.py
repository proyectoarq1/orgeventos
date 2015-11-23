from flask import Flask, render_template, flash, request, redirect, url_for, session, make_response, current_app
from flask_restful import Resource
from db.adapter_selected import adapter
from formularios.usuario_form import UserForm
import os


class RegisterController(Resource):
	def get(self):
		form = UserForm(request.form)
		headers = {'Content-Type': 'text/html'}
		return make_response(render_template('register.html', form=form, editar=False),200,headers)

	def post(self):
		form = UserForm(request.form)
		if form.validate():
			adapter.create_user(form)
			current_app.logger.info('El usuario se creo con exito')
			return redirect(url_for('login'))
		else :
			current_app.logger.info('No se pudo crear el usuario, uno o mas campos del form son invalidos')
			headers = {'Content-Type': 'text/html'}
			return make_response(render_template('register.html', form=form, editar=False),200,headers)