from flask import Flask, render_template, make_response, current_app, flash
from flask_restful import Resource
from db.models import User, Session
from db.adapter import adapter
from flask import request, redirect, url_for, session, abort
from flask.ext.login import LoginManager, login_user , current_user , login_required
import os

def doLogin():
  session=Session()
  username = request.form['username']
  password = request.form['password']
  registered_user = session.query(User).filter_by(username=username,password=password).first()
  if registered_user is None:
    current_app.logger.error('login user  ')
    flash('Username or Password is invalid' , 'error')
    return abort(404)#redirect(url_for('login'))
  current_app.logger.info('login user : ')
  login_user(registered_user)
  flash('Logged in successfully','success')

class LoginController(Resource):
    def get(self):
    	headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html'),200 ,headers)

    def post(self):
    	doLogin()
    	return redirect(request.args.get('next') or url_for('perfil'))

