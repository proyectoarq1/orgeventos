
from mongoengine import *
import mongo
import datetime

url = dbsettings.MONGO_DATABASE["url_conection"]
connect('pruebados', host=url)

class Usuario(Document):
    nombre = StringField()

class User(Base):
    username = StringField()
    password = StringField()
    email = StringField()
    registered_on = mongo.DateTimeField()
 
    def __init__(self , username , password , email):
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
        return unicode(self["_id"])) # revisar
 
    def __repr__(self):
        return '<User %r>' % (self.username)

class Evento(Document):
	nombre = StringField()
	organizador = StringField()
	descripcion = StringField()
    fecha = mongo.DateTimeField()
    asistiran = IntField(default=0)
    organizador_id = ReferenceField(Usuario)


