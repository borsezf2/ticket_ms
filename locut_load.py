from locust import HttpUser, task, between
import random

class LoadTestUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def load_test(self):
        endpoints = [
            "/register",
            "/login",
            "/login_2",
            "/search_train",
            "/book_train",
            "/search_ticket",
            "/ticket_pdf",
            "/cancel_ticket",
            "/add_train",
            "/update_train",
            "/add_ads"
        ]
        endpoint = random.choice(endpoints)
        self.client.get(endpoint)

if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py --host=http://10.5.16.212:9050")



# locust -f locustfile.py --host=http://10.5.16.212:9050
