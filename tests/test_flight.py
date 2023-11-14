import unittest
from flask import current_app
import json
from app import create_app
import logging

class FlightTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')

        self.logger = logging.getLogger("Test conversation:")
        self.logger.setLevel(level=logging.DEBUG)

    
    def test_insert_new_flight(self):
        """
            Use case:
            user: Hello
            bot:   Hi

            bot:Please choose one of the following tasks: 
                1: Register a new flight.
                2: Create a restaurant ontology.
                3: Test model ontology.
               Enter a corresponding number for a wanted option:

            user: 1
            bot:  Enter the flight name (flight descriptor).      
            bot:  LH1234 

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

        self.logger.debug('test +++ 2. 1')
        response = tester.post('/chatresponse', 
                            data=json.dumps(dict(message='1')),
                            content_type='application/json')
        result = json.loads(response.text)
        for sentence in result:
            self.logger.debug('test --- 2. ' + sentence.get('response'))
            
        self.logger.debug('test +++ 3. LH1234')
        response = tester.post('/chatresponse', 
                            data=json.dumps(dict(message='LH1234')),
                            content_type='application/json')
        result = json.loads(response.text)
        for sentence in result:
            self.logger.debug('test --- 3. ' + sentence.get('response'))
        self.assertEqual(type('Insert data for '), type(result[0].get('response')))
