from flask import Flask, render_template, flash, request, redirect, url_for, session, make_response
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
			return redirect(url_for('login'))
		else :
			headers = {'Content-Type': 'text/html'}
			return make_response(render_template('register.html', form=form, editar=False),200,headers)