"""
    test_api.py
    usage:

    python -m unittest discover -p test_api.py
"""

import json
import unittest

from app import app
# set our application to testing mode
app.testing = True


class TestApi(unittest.TestCase):

    def test_main(self):
        with app.test_client() as client:
            # send data as POST form to endpoint
            sent = {'return_url': 'my_test_url'}
            result = client.post(
                '/',
                data=sent
            )
            # check result from server with expected data
            self.assertEqual(
                result.data,
                json.dumps(sent)
            )