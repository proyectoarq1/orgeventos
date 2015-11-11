from flask import Flask, render_template, make_response, current_app
from flask_restful import Resource
from flask import redirect, url_for
from flask.ext.login import logout_user, login_required
import os

class LogoutController(Resource):
	@login_required
	def get(self):
  		current_app.logger.info('logout user  ')
  		logout_user()
  		#print current_user.is_authenticated
  		return redirect(url_for('home')) 