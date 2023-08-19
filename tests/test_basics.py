import unittest
from flask import current_app
import json
from app import create_app
import logging

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')

        self.logger = logging.getLogger("Test conversation:")
        self.logger.setLevel(level=logging.DEBUG)

    def test_indexpage(self):
        tester = self.app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    def test_insert_new_instance(self):
        """
            Use case:
            user: Hello
            bot:   Hi

            bot:Please choose one of the following tasks: 
                1: Register a new flight.
                2: Create a restaurant ontology.
                3: Test model ontology.
               Enter a corresponding number for a wanted option:

            user: 2
            user:  Insert data for Restaurant name          
            bot:  Halkidiki

        """
        tester = self.app.test_client(self)
        self.logger.debug('test +++ 1. Hello')
        response = tester.post('/chatresponse', 
                            data=json.dumps(dict(message='Hello')),
                            content_type='application/json')
        result = json.loads(response.text)
        for sentence in result:
            self.logger.debug('test --- 1. ' + sentence.get('response'))
        # First element of the response is an answer to Hello
        # Second element in the json list is the answer to the question which is an empty string
        # and this way is used to activate Ontochat LogicAdapter
        self.assertIn(result[0].get('response'), ['Hi','Hello', 'Greetings!']) 
        self.assertRegex(result[1].get('response'),
                         r".* Enter a corresponding number for a wanted option:") 

        self.logger.debug('test +++ 2. 2')
        response = tester.post('/chatresponse', 
                            data=json.dumps(dict(message='2')),
                            content_type='application/json')
        result = json.loads(response.text)
        for sentence in result:
            self.logger.debug('test --- 2. ' + sentence.get('response'))
            
        self.logger.debug('test +++ 3. Halkidiki')
        response = tester.post('/chatresponse', 
                            data=json.dumps(dict(message='Halkidiki')),
                            content_type='application/json')
        result = json.loads(response.text)
        for sentence in result:
            self.logger.debug('test --- 3. ' + sentence.get('response'))
        self.assertEqual(type('Insert data for '), type(result[0].get('response')))

