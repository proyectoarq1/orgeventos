from flask import Flask, render_template
from flask_login import login_required
from db.models import Session, Usuario, Evento
from formularios.evento_form import EventoForm
from db.adapter import adapter
import datetime
from flask import request, redirect, url_for, session
import os
 
app = Flask(__name__)      
 
app.config['SECURITY_POST_LOGIN'] = '/profile'


def hacer_usuario_y_ejemplo():
	db_session = Session()
	usuario = Usuario(nombre="Cosme Fulanito")
	db_session.add(usuario)
	db_session.commit()
	print usuario.id
	evento1 = Evento(organizador=usuario.nombre,
					nombre="Evento uno",
					descripcion="Me gustaria poder organizar una juntada", 
					fecha=datetime.date.today(), 
					asistiran=0, 
					organizador_id=usuario.id)
	evento2 = Evento(organizador=usuario.nombre,
					nombre="Evento dos",
					descripcion="Hagamos tambien otra juntada mas", 
					fecha=datetime.date.today(), 
					asistiran=0, 
					organizador_id=usuario.id)
	print evento1.organizador_id
	db_session.add(evento1)
	db_session.add(evento2)
	db_session.commit()
	session['usuario_id'] = usuario.id


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
  usuario = adapter.get_usuario(session['usuario_id'])
  eventos = adapter.obtener_eventos_asignados(session['usuario_id'])

  return render_template('perfil.html', usuario=usuario, eventos=eventos)

 
if __name__ == '__main__':
  port = os.getenv('PORT', '5000')

  app.secret_key = 'super secret key'
  app.run(host='0.0.0.0',port=int(port),debug=True)