from locust import HttpUser, task, constant_pacing, LoadTestShape
from config import cfg


class BackendUser(HttpUser):
    wait_time = constant_pacing(cfg.pacing_sec)
    host = "https://www.google.co.uk/"

    @task
    def health_load(self):
        self.client.get(url="")