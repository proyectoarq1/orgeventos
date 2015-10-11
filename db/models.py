from django.db import models
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref

from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.engine.url import URL
from sqlalchemy_utils import database_exists, create_database

import dbsettings

url = os.getenv('DATABASE_URL', URL(**dbsettings.DATABASE))
engine = create_engine(url)

if (os.getenv('DATABASE_URL') is None) and not database_exists(engine.url):
	print "INFO: Creating database ", dbsettings.DATABASE["database"]
	create_database(engine.url)

#print(database_exists(engine.url))


Session = sessionmaker(bind=engine)
Base = declarative_base()

class Usuario(Base):
	__tablename__ = 'usuario'
	id = Column(Integer, primary_key=True)
	nombre = Column(String(500))

class Evento(Base):
	__tablename__ = 'evento'
	id = Column(Integer, primary_key=True)
	nombre = Column(String(100))
	organizador = Column(String(100))
	descripcion = Column(String(700))
	fecha = Column(DateTime)
	asistiran = Column(Integer())
	organizador_id = Column(Integer, ForeignKey('usuario.id'))

class Invitacion(Base):
	__tablename__ = 'invitacion'
	evento_id = Column(Integer, primary_key=True)
	usuario_id = Column(Integer, primary_key=True)


if __name__ == '__main__':
	#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dbsettings")
	#session = Session()
	Base.metadata. drop_all(engine)
	Base.metadata.create_all(engine)