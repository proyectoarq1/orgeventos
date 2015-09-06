from django.db import models
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref

from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.engine.url import URL

import dbsettings

from flask.ext.social import Social
from flask.ext.social.datastore import SQLAlchemyConnectionDatastore


url = os.getenv('DATABASE_URL', URL(**dbsettings.DATABASE))
engine = create_engine(url)


Session = sessionmaker(bind=engine)
Base = declarative_base()

class Usuario(Base):
	__tablename__ = 'usuario'
	id = Column(Integer, primary_key=True)
	nombre = Column(String(500))
	nombre_usuario_facebook= Column(String(500))
	organizador = relationship("Evento", backref="usuario")

class Evento(Base):
	__tablename__ = 'evento'
	id = Column(Integer, primary_key=True)
	nombre = Column(String(100))
	organizador = Column(String(100))
	descripcion = Column(String(700))
	fecha = Column(DateTime)
	asistiran = Column(Integer())
	organizador_id = Column(Integer, ForeignKey('usuario.id'))

#class Connection(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
#    provider_id = db.Column(db.String(255))
#    provider_user_id = db.Column(db.String(255))
#    access_token = db.Column(db.String(255))
#    secret = db.Column(db.String(255))
#    display_name = db.Column(db.String(255))
#    profile_url = db.Column(db.String(512))
#    image_url = db.Column(db.String(512))
#    rank = db.Column(db.Integer)

#Security(app, SQLAlchemyUserDatastore(db, User, Role))
#Social(app, SQLAlchemyConnectionDatastore(db, Connection))


if __name__ == '__main__':
	#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dbsettings")
	#session = Session()
	Base.metadata.create_all(engine)