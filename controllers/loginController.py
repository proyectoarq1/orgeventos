from flask import Flask, render_template, make_response, current_app, flash
from flask_restful import Resource
from db.adapter_selected import adapter
from flask import request, redirect, url_for, abort
from flask.ext.login import LoginManager, login_user , current_user , login_required
import os

class LoginController(Resource):
    def get(self):
    	headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html'),200 ,headers)

    def post(self):
      username = request.form['username']
      password = request.form['password']
      registered_user = adapter.get_user_by_name_and_pass(username,password)
      current_app.logger.info(registered_user)
      if registered_user is None:
        current_app.logger.error('login user is not reigster ')
        flash('El nombre de usario o la password ingresada es invalida' , 'error')
        #abort(400)
        return redirect(url_for('login'))
      current_app.logger.info('login user : ' + registered_user.username)
      login_user(registered_user,True)
      return redirect(request.args.get('next') or url_for('perfil'))

