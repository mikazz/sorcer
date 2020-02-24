from flask_testing import TestCase
from flask import Flask
import unittest
import json
from app import app
import request


class BaseTestCase(TestCase):
    def create_app(self):
        #from app import app
        return app

        # app = Flask(__name__)
        # app.config['TESTING'] = True
        # return app
        #

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass


class TestMainBlueprint(BaseTestCase):
    def test_index(self):
        # Ensure Flask is setup # Ensure Connection to Redis is established.
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_index(self):
        response = self.client.get("/rq", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_api(self):
        """
        https://flask.palletsprojects.com/en/1.1.x/testing/

        :return:
        """

        with app.test_client() as c:
            response = c.post('/job', json={
                'page_url': 'https://www.google.com/', 'function': 'get_text'
            })

            print(response)
            json_data = response.get_json()

            #assert verify_token(email, json_data['token'])


    # def test_successful_post_job(self):
    #     """
    #         Add Job
    #     """
    #
    #     # Given
    #     payload = json.dump({
    #         "page_url": "https://www.google.com/",
    #         "function": "get_text"
    #     })
    #
    #     print(self.app)
    #     print(payload)
    #
    #     # When
    #     #response = self.app.post('/job', content_type='application/json', data=payload)
    #     response = self.client.post('/job', content_type='application/json', data=payload)
    #     print(response)
    #
    #     # Then
    #     #self.assertEqual(str, type(response.json['id']))
    #
    #     #self.assertEqual("success", type(response.json['status']))
    #     #self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()
