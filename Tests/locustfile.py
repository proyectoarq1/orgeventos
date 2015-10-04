from locust import HttpLocust, TaskSet

#def login(l):
#    l.client.post("/login", {"username":"ellen_key", "password":"education"})

def home(l):
    l.client.get("/")

def perfil(l):
    l.client.get("/perfil")

class UserBehavior(TaskSet):
    tasks = {home:10, perfil:5}

    def on_start(self):
        #login(self)
        pass

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000