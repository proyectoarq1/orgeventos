from sqlalchemy.ext.declarative import DeclarativeMeta
import json
from models import Usuario, Session

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
                    print e
            # a json-encodable dict
            fields = self.agregar__id(fields)
            print fields
            return fields

    def agregar__id(self, fields):
        fields["_id"] = fields["id"]
        return fields



        return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':

    db_session = Session()
    usuario = Usuario(nombre="usuario_nombre")
    db_session.add(usuario)
    db_session.commit()

    print usuario
    print json.loads(json.dumps(usuario, cls=AlchemyEncoder))