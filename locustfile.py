from locust import HttpUser, task, between

class LibraryAPIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_all_books(self):
        with self.client.get("/books/", name="Get Books", catch_response=True) as response:
            
            if response.status_code in [200, 401]:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")