from locust import HttpLocust, TaskSet

def login(l):
    l.client.post("/login", {"username":"Test1", "password":"test1"})

def home(l):
    l.client.get("/")

def perfil(l):
    l.client.get("/perfil")

def nuevo_evento(l):
    l.client.get("/nuevo_evento")

class UserBehavior(TaskSet):
    tasks = {home:1, perfil:1, nuevo_evento:1, perfil:2, nuevo_evento:1, home: 3}

    def on_start(self):
        login(self)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000