from locust import HttpLocust, TaskSet
import random



def crear_evento(l):
    login(l)
    nombres = ['Mi cumple', 'Navidad falsa en casa', 'Asado', 'Previa del sabado', 'Juntada', 'Dia del amigo', 'Cumple Sorpresa', 'Recibida', 'Bautismo', 'Mi divorcio', 'Despedida', 'Reencuentro 2015', 'Merienda', 'Fulbito']
    descripcciones = ['Quiero que vengan todos asi festejamos juntos', 'Para que vivamos un momento en familia', 'Hace mucho que no nos juntamos gente y estaria bueno hacerlo', 'Quiero que festejemos juntos', 'Organicemosnos cuanto antes porque despues colgamos', 'Quiero compartir mi alegria con ustedes', 'Organicemos una buena Joda', 'Asi somos mas de cuatro alguna vez']
    horas = ['07:00','00:00', '15:00', '22:00', '21:00', '16:45', '03:00', '23:00']
    fechas = ['23/03/2016','10/12/2015','01/01/2016','25/12/2015','20/07/2016','28/02/2016','03/08/2016']
    ubicaciones = ['Manantiales Chicos', 'Mendoza', 'General Alvear', 'Departamento de Cafayate', 'Cafayate','Gobernador Benegas', 'Azcuenaga', 'Olaeta', 'Los Condores', 'De la Garma', 'La Calera', 'Lartigau', 'Arroyo Cabral', 'Gobernador Gregores', 'Santa Regina', 'Amadores', 'Guerrico', 'San Carlos Sur', 'Alto de la Piedra', 'Puerto Ruiz', 'El Pueblito']    
    categorias = ['Publico','Privado']
    url = ['http://unaurl.com']
    l.client.post('/nuevo_evento',
        {'hora': random.choice(horas),
        'categoria':random.choice(categorias), 
        'descripcion': random.choice(descripcciones), 
        'ubicacion': random.choice(ubicaciones),
        'nombre': random.choice(nombres),
        'fecha': random.choice(fechas),
        'url_imagen': random.choice(url)})

def register(l):
    l.client.post("/register", {"username":"test", "password":"test111", "confirm":"test111", "email": "test1@test1.com"})

def login(l):
    l.client.post("/login", {"username":"test2", "password":"test22"})

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
    tasks = {nuevo_evento:1,crear_evento:1}

    #def on_start(self):
    #    register(self)
    #    login(self)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000