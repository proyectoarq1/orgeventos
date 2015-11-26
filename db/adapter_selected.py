import os

db_seleccionada = os.getenv('TIPO_BASE_DE_DATOS', 'MySQL')

if db_seleccionada=='MongoDB':
	from mongoAdapter import MongoAdapter
	adapter = MongoAdapter()
else:
	from sqlAdapter import MySQLAdapter
	adapter = MySQLAdapter()