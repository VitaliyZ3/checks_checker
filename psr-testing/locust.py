from locust import HttpUser, task, between
import json

f = open("./payloads/invoice_create.json")

invoice_create_data = json.load(f)

class BackendUser(HttpUser):
    wait_time = between(1,5)

    @task
    def health_page(self):
        self.client.post(url="/invoice", data=json.dumps(invoice_create_data))
