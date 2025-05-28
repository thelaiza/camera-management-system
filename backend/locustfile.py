from locust import HttpUser, task, between

class ApiUser(HttpUser):
    wait_time = between(1, 2) 

    @task(1) # Peso 1
    def get_api_home(self):
        self.client.get("/api/api/") 

    @task(2)
    def get_cameras(self):
        self.client.get("/api/cameras/") 

    @task(2) 
    def get_usuarios(self):
        self.client.get("/api/usuarios/") 

