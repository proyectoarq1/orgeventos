from mongoalchemy.session import Session
from bson.objectid import ObjectId
from mongoalchemy.document import Document, Index
from mongoalchemy.fields import *
import datetime
import os, json
from alchemy_encoder import AlchemyEncoder, MongoAlchemyEncoder

import dbsettings

url = os.getenv('DATABASE_URL', dbsettings.MONGO_DATABASE["url_conection"])

db_seleccionada = os.getenv('TIPO_BASE_DE_DATOS', 'MySQL')

session=None
if db_seleccionada=='MongoDB':
    session = Session.connect("prueba3")

#mongod --config c:\mongodb\mongo.config

class User(Document):
    config_collection_name = "users"
    username =  StringField()
    username_index = Index().ascending('username').unique()
    password = StringField()
    email = StringField()
    email_index = Index().ascending('email').unique()
    registered_on = DateTimeField(default=datetime.datetime.utcnow())
    
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.mongo_id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)

class Evento(Document):
    config_collection_name = 'eventos'
    nombre = StringField()
    organizador = StringField()
    descripcion = StringField()
    ubicacion =  StringField()
    categoria =  StringField()
    fecha = DateTimeField()
    asistiran = IntField(default=0)
    organizador_id = ObjectIdField()
    invitados = ListField(ObjectIdField(),required=False,default=[])

if __name__ == '__main__':
    #session.clear_collection(User)
    user=User(username='Jeff31', password='Jenkins31', email="algoalgo31")
    session.save(user)
    print user.get_id()
    user1 = session.query(User).filter_by(mongo_id=user.get_id()).first()
    print "aaaaaaaaa"
    print user1

    print json.loads(json.dumps(user1, cls=MongoAlchemyEncoder))
    
    members = [attr for attr in dir(User()) if not callable(attr) and not attr.startswith("_")]
    
    print user1.get_fields().keys()
    
    user1 = session.query(User).filter_by(mongo_id=user.get_id()).first()
    print user1
    evento = Evento(organizador="lalalalala",
                        organizador_id=user1.get_id(),
                        nombre="form.nombre.data",
                        fecha=datetime.datetime.utcnow(),
                        descripcion="form.descripcion.data",
                        asistiran=0)
    session.save(evento)
    evento = session.query(Evento).filter_by(mongo_id=evento.mongo_id).first()
    print evento.invitados
    evento.invitados.append("3829382938293892")
    evento.invitados.append("77777")
    print evento.invitados
    session.save(evento)
    evento = session.query(Evento).filter_by(mongo_id=evento.mongo_id).first()
    print evento.invitados
    evento.invitados.remove("3829382938293892")
    session.save(evento)
    evento = session.query(Evento).filter_by(mongo_id=evento.mongo_id).first()
    print evento.invitados
    print json.loads(json.dumps(evento, cls=MongoAlchemyEncoder))
    evento = session.query(Evento).filter({ "invitados": [ "3829382938293892" ] }).all()
    evento = session.query(Evento).filter({ "invitados": [ "3829382938293892" ] }).all()
    for e in evento:
        print e.invitados
    eeee = session.query(Evento).all()
    print "..................."
    for e in eeee:
        print e.invitados
