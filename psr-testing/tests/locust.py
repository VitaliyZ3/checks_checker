from locust import HttpUser, task, constant_pacing
import json
from config import cfg

f = open("./payloads/invoice_create.json")

invoice_create_data = json.load(f)


class BackendUser(HttpUser):
    wait_time = constant_pacing(cfg.pacing_sec)
    host = cfg.api_host

    @task
    def create_invoice(self):
        self.client.post(url="/invoice", data=json.dumps(invoice_create_data))
