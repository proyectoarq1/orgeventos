from django.db import models
import os
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref

from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Time
from sqlalchemy.types import Boolean
from sqlalchemy.engine.url import URL
from sqlalchemy_utils import database_exists, create_database
from utils.Asistencia import *
from sqlalchemy_enum34 import EnumType

import dbsettings

url = os.getenv('DATABASE_URL', URL(**dbsettings.DATABASE))
engine = create_engine(url)

if (os.getenv('DATABASE_URL') is None) and not database_exists(engine.url):
	print "INFO: Creating database ", dbsettings.DATABASE["database"]
	create_database(engine.url)

#print(database_exists(engine.url))


Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column('user_id',Integer , primary_key=True)
    username = Column('username', String(20), unique=True , index=True)
    password = Column('password' , String(10))
    email = Column('email',String(50),unique=True , index=True)
    registered_on = Column('registered_on' , DateTime)
 
    def __init__(self , username ,password , email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.datetime.utcnow()
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)

class Evento(Base):
    __tablename__ = 'evento'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    organizador = Column(String(100))
    categoria = Column(String(50))
    descripcion = Column(String(700))
    ubicacion = Column(String(700))
    url_imagen = Column(String(700))
    fecha = Column(Date)
    hora = Column(String(5))
    asistiran = Column(Integer(), default=0)
    organizador_id = Column(Integer, ForeignKey('users.user_id'))

class Invitacion(Base):
    __tablename__ = 'invitacion'
    evento_id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, primary_key=True)
    asiste = Column(EnumType(Asistencia,name="asiste"))

class Requerimiento(Base):
    __tablename__ = 'requerimientos'
    id = Column(Integer, primary_key=True)
    evento_id = Column(Integer)
    nombre = Column(String(50))
    descripccion = Column(String(200))
    cantidad = Column(Integer, default=1)

class RequerimientoAsignado(Base):
    __tablename__ = 'requerimientos_asignados'
    id = Column(Integer, primary_key=True)
    requerimiento_id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, primary_key=True)
    cantidad = Column(Integer, default=1)
    
if __name__ == '__main__':
	#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dbsettings")
	#session = Session()
	#Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)