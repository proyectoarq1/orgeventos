from flask import Flask, render_template
from flask_login import login_required
from db.models import Session, Usuario, Evento
from formularios.evento_form import EventoForm
import datetime
from flask import request, redirect, url_for, session

 
app = Flask(__name__)      
 
app.config['SECURITY_POST_LOGIN'] = '/profile'


def hacer_usuario_y_ejemplo():
	db_session = Session()
	usuario = Usuario(nombre="Cosme Fulanito")
	db_session.add(usuario)
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
	db_session = Session()
	usuario = db_session.query(Usuario).filter_by(id=session['usuario_id']).first()
	if request.method == 'POST' and form.validate():
		print form.data
		print form.nombre
		evento = Evento(organizador=usuario.nombre,
						organizador_id=usuario.id,
						nombre=form.nombre.data,
						fecha=form.fecha.data,
						descripcion=form.descripcion.data,
						asistiran=0)
		db_session.add(evento)
		db_session.commit()
		return redirect(url_for('perfil'))
	return render_template('nuevo_evento.html', usuario=usuario, form=form)

@app.route('/evento')
def evento():
	db_session = Session()
	id_evento = request.args.get('evento')
	evento = db_session.query(Evento).filter_by(id=id_evento).first()
	return render_template('evento.html',evento=evento)

@app.route('/perfil')
def perfil():
  db_session = Session()
  usuario = db_session.query(Usuario).filter_by(id=session['usuario_id']).first()
  eventos_usuario = db_session.query(Evento).filter_by(organizador_id=session['usuario_id']).all()
  eventos = []
  print eventos_usuario
  for e in eventos_usuario:
  	eventos.append(e)

  return render_template('perfil.html', usuario=usuario, eventos=eventos)



@app.route('/profile')
@login_required
def profile():
    return render_template(
        'profile.html',
        content='Profile Page',
        facebook_conn=social.facebook.get_connection())
 
if __name__ == '__main__':
  app.secret_key = 'super secret key'
  app.run(debug=True)