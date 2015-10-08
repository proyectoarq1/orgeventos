from flask import Flask, render_template, flash, abort 
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required

from db.models import Session, Usuario, Evento, User
from formularios.evento_form import EventoForm
from db.adapter import adapter
import datetime
from flask import request, redirect, url_for, session
import os, json
import logging
from logging.handlers import TimedRotatingFileHandler
 
app = Flask(__name__)      

app.config.from_object('config')
 
app.config['SECURITY_POST_LOGIN'] = '/profile'

formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
file_handler = TimedRotatingFileHandler(app.config['LOG_PATH'], when="D", backupCount=7)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)
 
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  return adapter.get_user_by_id(user_id)

def hacer_usuario_y_ejemplo():
	
	usuario = adapter.crear_usuario("Cosme Fulanito")
	usuario_id = adapter.get_id(usuario)

	form_evento1 = EventoForm(nombre="Evento uno", fecha=None, descripcion="Me gustaria poder organizar una juntada")
	form_evento2 = EventoForm(nombre="Evento dos", fecha=None, descripcion="Hagamos tambien otra juntada mas")

	e1 = adapter.crear_evento(usuario_id,form_evento1)
	e2 = adapter.crear_evento(usuario_id,form_evento2)

	
	session['usuario_id'] = usuario_id

@app.route('/register' , methods=['GET','POST']) # siguiente|
def register():
  if request.method == 'GET':
      return render_template('register.html')
  username = request.form['username']
  password = request.form['password']
  email = request.form['email']
  adapter.create_user(username, password, email)
  flash('User successfully registered','success')
  return redirect(url_for('login'))
 
@app.route('/login',methods=['GET','POST'])
def login():
  session=Session()
  if request.method == 'GET':
      return render_template('login.html')
  username = request.form['username']
  password = request.form['password']
  registered_user = session.query(User).filter_by(username=username,password=password).first()
  if registered_user is None:
    app.logger.error('login user  ')
    flash('Username or Password is invalid' , 'error')
    return redirect(url_for('login'))
  app.logger.info('login user : ')
  login_user(registered_user)
  flash('Logged in successfully','success')
  return redirect(request.args.get('next') or url_for('perfil'))

@app.route('/logout')
def logout():
  app.logger.info('logout user  ')
  logout_user()
  #print current_user.is_authenticated
  return redirect(url_for('home')) 

@app.route('/')
def home():
  hacer_usuario_y_ejemplo()
  return render_template('home.html',usuario=session['usuario_id'])

@app.route('/nuevo_evento', methods=['GET', 'POST'])
def nuevo_evento():
	
	form = EventoForm(request.form)
	if request.method == 'POST' and form.validate():
		adapter.crear_evento(session['usuario_id'],form)
		return redirect(url_for('perfil'))
	return render_template('nuevo_evento.html', form=form)

@app.route('/evento/<evento_id>')
def evento(evento_id):	
	evento = adapter.get_evento(session['usuario_id'],evento_id)
	return render_template('evento.html',evento=evento)

@app.route('/perfil')
def perfil():
  flash(current_user.username)
  app.logger.info('perfil page ')
  usuario = adapter.get_usuario(session['usuario_id'])
  eventos = adapter.obtener_eventos_asignados(session['usuario_id'])

  return render_template('perfil.html', usuario=usuario, eventos=eventos)

 
if __name__ == '__main__':
  port = os.getenv('PORT', '5000')

  app.secret_key = 'super secret key'
  app.logger.info('Run Application')
  app.run(host='0.0.0.0',port=int(port),debug=True)
  #hacer_usuario_y_ejemplo()