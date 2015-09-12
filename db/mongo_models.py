
from mongoengine import *
import mongo
import datetime

url = dbsettings.MONGO_DATABASE["url_conection"]
connect('pruebados', host=url)

class Usuario(Document):
    nombre = StringField()

class Evento(Document):
	nombre = StringField()
	organizador = StringField()
	descripcion = StringField()
    fecha = mongo.DateTimeField()
    asistiran = IntField(default=0)
    organizador_id = ReferenceField(Usuario)


