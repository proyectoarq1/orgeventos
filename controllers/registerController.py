from flask import Flask, render_template, flash, request, redirect, url_for, session, make_response
from flask_restful import Resource
from db.adapter_selected import adapter
import os

def doRegister():
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']
	adapter.create_user(username, password, email)
	flash('User successfully registered','success')

class RegisterController(Resource):
    def get(self):
    	headers = {'Content-Type': 'text/html'}
        return make_response(render_template('register.html'),200,headers)

    def post(self):
    	doRegister()
    	return redirect(request.args.get('next') or url_for('login'))