from locust import HttpLocust, TaskSet

def crear_evento(l):
    l.client.post('/nuevo_evento',{'hora': '03:50','categoria':'Publico', 'descripcion': 'Un evento de prueba con Mongodb', 'ubicacion':'Mendoza', 'nombre':'Un evento nuevo', 'fecha': '02/09/2008', 'url_imagen':'http://unaurl.com'})

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
    tasks = {login:1,nuevo_evento:1,crear_evento:1}

    #def on_start(self):
    #    register(self)
    #    login(self)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000