from mongoAdapter import MongoAdapter
from sqlAdapter import MySQLAdapter
import os

db_seleccionada = os.getenv('TIPO_BASE_DE_DATOS', 'MySQL')

if db_seleccionada=='MongoDB':
	adapter = MongoAdapter()
else:
	adapter = MySQLAdapter()