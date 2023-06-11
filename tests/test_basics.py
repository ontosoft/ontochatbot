import unittest
from flask import current_app
import json
from app import create_app

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')

    def test_indexpage(self):
        tester = self.app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    def test_insert_new_instance(self):
        tester = self.app.test_client(self)
        response = tester.post('/chatresponse', 
                            data=json.dumps(dict(message='Hello')),
                            content_type='application/json')
        result = json.loads(response.text)
        self.assertIn(result[0].get('response'), ['Hi','Hello', 'Greetings!']) 
        # Second element in the whole json list is the answer to the question which is an empty string
        # and this should activate our ontochat LogicAdapter
        self.assertEqual('Insert data for Restaurant name', result[1].get('response'))
        response = tester.post('/chatresponse', 
                            data=json.dumps(dict(message='Halkidiki')),
                            content_type='application/json')
        result = json.loads(response.text)
        self.assertEqual('Insert data for ', result[0].get('response'))

