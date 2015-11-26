from locust import HttpLocust, TaskSet
import random



def crear_evento(l):
    login(l)
    nombre_descripcion_foto = [
        {"nombre": 'Navidad falsa en casa', "descripcion": 'Como navidad nada mas que otro dia y en familia' , "foto": "http://www.fondox.net/wallpapers/arreglos-para-navidad-3051.jpg" },
        {"nombre": 'Asado', "descripcion": 'Hagamo un asado, tomemo fernet' , "foto": "http://www.elsigloweb.com/uploads/editorial/2015/04/03/imagenes/81981_asado-parrilla.jpg" },
        {"nombre": 'Previa del sabado', "descripcion":'Yo pongo la casa y ustedes la diversion, traigan bebidas' , "foto": "http://7boom.mx/wp-content/uploads/2014/11/N56ug56eb56un56il56.jpeg" },
        {"nombre": 'Juntada', "descripcion": 'Hace mucho que no nos juntamos todas, podemos ponernos deacuerdo para la fecha' , "foto": "http://2.bp.blogspot.com/-NGNEINi-dQk/VFOWUx7qmgI/AAAAAAAAIWs/phHqDL6AUko/s1600/halloween-witches-vintage-ypalt5th.jpg" },
        {"nombre": 'Dia del amigo', "descripcion": 'Excusa persfecta para que estemos todas' , "foto": "http://www.red92.com/images/uploaded/articles/4349.jpg" },
        {"nombre": 'Cumple Sorpresa', "descripcion": 'Shhhh acuerdense que es sorpresa!!' , "foto": "http://sp3.fotolog.com/photo/51/7/40/sick_maggot/1258280880362_f.jpg" },
        {"nombre": 'Recibida', "descripcion": 'Me recibo y quiero estar con todos ustedes en este momento' , "foto": "http://arq.clarin.com/arquitectura/campus-UNQ-recta-final_CLAIMA20110927_0009_19.jpg" },
        {"nombre": 'Bautismo', "descripcion": 'Bautismo del gordito', "foto": "https://s-media-cache-ak0.pinimg.com/736x/69/68/df/6968df7ebf5aa79c7d77bcffd63e9518.jpg" },
        {"nombre": 'Mi divorcio', "descripcion": 'Estas cosas tambien hay que festejarlas!' , "foto": "http://www.losandes.com.ar/files/image/15/09/image55f4341aac3829.85641505.jpg" },
        {"nombre": 'Despedida', "descripcion": 'Despedida de soltera de Natii' , "foto": "http://3.bp.blogspot.com/-xhsFT4XAHOE/T3mKA23njTI/AAAAAAAAGK8/1zqq56NLZe4/s400/II.png" },
        {"nombre": 'Reencuentro 2015', "descripcion": 'Reencuentro egresados ICR 2008' , "foto": "http://globedia.com/imagenes/noticias/2012/6/1/american-pie-reencuentro-simplemente-palabras_1_1239672.jpg" },
        {"nombre": 'Fulbito', "descripcion": 'A ver si asi somos mas de 4 alguna vez', "foto": "http://thumbs.dreamstime.com/x/soccer-balls-23191644.jpg" },
        {"nombre": 'Merienda', "descripcion": 'Merienda de abuelas en lo de pocha' , "foto": "http://static.guiainfantil.com/pictures/recetas/5505-4-muffins-o-magdalenas-de-arandanos-para-la-merienda-de-los-ninos.jpg" } ]
    horas = ['07:00','00:00', '15:00', '22:00', '21:00', '16:45', '03:00', '23:00']
    fechas = ['03/23/2016','10/12/2015','01/01/2016','12/12/2015','07/07/2016','02/28/2016','03/08/2016']
    ubicaciones = ['Manantiales Chicos', 'Mendoza', 'General Alvear', 'Departamento de Cafayate', 'Cafayate','Gobernador Benegas', 'Azcuenaga', 'Olaeta', 'Los Condores', 'De la Garma', 'La Calera', 'Lartigau', 'Arroyo Cabral', 'Gobernador Gregores', 'Santa Regina', 'Amadores', 'Guerrico', 'San Carlos Sur', 'Alto de la Piedra', 'Puerto Ruiz', 'El Pueblito']    
    categorias = ['Publico','Privado']

    datos = random.choice(nombre_descripcion_foto)

    l.client.post('/nuevo_evento',
        {'hora': random.choice(horas),
        'categoria':random.choice(categorias), 
        'descripcion': datos["descripcion"], 
        'ubicacion': random.choice(ubicaciones),
        'nombre': datos["nombre"],
        'fecha': random.choice(fechas),
        'url_imagen': datos["foto"]})

def register(l):
    l.client.post("/register", {"username":"test", "password":"test111", "confirm":"test111", "email": "test1@test1.com"})

def login(l):
    l.client.post("/login", {"username":"tatiana", "password":"tatiana"})

def home(l):
    l.client.get("/")

def perfil(l):
    l.client.get("/perfil")

def nuevo_evento(l):
    l.client.get("/nuevo_evento")

def logout(l):
    l.client.get("/logout")

class UserBehavior(TaskSet):
    #tasks = {login:1,home:1, perfil:1, nuevo_evento:1, perfil:2, nuevo_evento:1, crear_evento:1, home: 3}
    tasks = {nuevo_evento:1,crear_evento:1, home:3}

    #def on_start(self):
    #    register(self)
    #    login(self)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000