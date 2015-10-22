from sqlalchemy.ext.declarative import DeclarativeMeta
from mongoalchemy.document import Document
import json
from models import Usuario, Session
from mongoalchemy.fields import *

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError as e:
                    fields[field] = str(data)
            # a json-encodable dict
            fields = self.agregar__id(fields)

            return fields

    def agregar__id(self, fields):
        fields["_id"] = fields["id"]
        return fields



        return json.JSONEncoder.default(self, obj)

class MongoAlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, Document.__class__):
            out = {}
            for field in obj.get_fields().keys():
                data = obj.__getattribute__(field)
                try:
                    if isinstance(data, (list)):
                        print "encontre la lista"
                        print data
                        out[field] = [self.default(item) for item in data]
                    else:
                        json.dumps(data) # this will fail on non-encodable values, like other classes
                        out[field] = data
                except TypeError as e:
                    out[field] = str(data)
                    #print e
                    #if isinstance(data.__class__, ObjectId.__class__):
            self.agregar__id(out)
        else:
            out = str(obj)
        return out

    def agregar__id(self, out):
        out["_id"] = out["mongo_id"]
        return out

        return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':

    db_session = Session()
    usuario = Usuario(nombre="usuario_nombre")
    db_session.add(usuario)
    db_session.commit()

    print usuario
    print json.loads(json.dumps(usuario, cls=AlchemyEncoder))
