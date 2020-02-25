from flask_testing import TestCase
import unittest
from app import app


class BaseTestCase(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass


class TestMainBlueprint(BaseTestCase):
    def test_index(self):
        # Ensure Flask is setup # Ensure Connection to Redis is established.
        # When
        response = self.client.get("/", follow_redirects=True)
        # Then
        self.assertEqual(response.status_code, 200)

    def test_dashboard_index(self):
        # When
        response = self.client.get("/rq", follow_redirects=True)
        # Then
        self.assertEqual(response.status_code, 200)

    def test_get_jobs(self):
        # When
        response = self.client.get("/jobs", follow_redirects=True)
        # Then
        self.assertEqual(response.status_code, 200)

    # def test_long_job(self):
    #     """
    #         curl -X POST -F "duration=3" http://127.0.0.1:5000/long_job
    #     """
    #     response = self.client.post("/job", follow_redirects=True)
    #     print(response)

    def test_post_job(self):
        """
            Test Add Job
        """

        # Given
        payload = {
            "page_url": "https://www.google.com/",
            "function": "get_text"
        }

        # When
        response = self.client.post('/job', data=payload)
        print(response)

        # Then
        self.assertEqual("success", response.json['status'])
        self.assertEqual(202, response.status_code)


if __name__ == "__main__":
    unittest.main()
