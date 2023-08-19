from chatterbot import ChatBot
#from chatterbot.trainers import ListTrainer
#from chatterbot.trainers import ChatterBotCorpusTrainer
from . import ontoadapter
from owlready2 import get_ontology, World
from owlready2 import Thing
from pathlib import Path

import logging 
logging.basicConfig(level=logging.INFO)

#The following lines were necessary to import our  
# ontology based logical adapter from the current path
import os.path
import sys
current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_directory)
path = Path.cwd() # Loading obop ontology from the main directory of the project
onto_inferences = get_ontology('http://example.com/obop_inferences.owl')
# all ontologies had to be inserted in separate worlds in order to search only that ontology
# if the world is not specified then the defauld_world is used
# OBOP ontology is imported in all worlds separately
world_flights = World()
flight_model = world_flights.get_ontology(str(path.joinpath('ontologies','flight_model.owl'))).load()
obop_world1 = world_flights.get_ontology(str(path.joinpath('ontologies','obop.owl'))).load()
world_restaurant = World()
restaurant_model = world_restaurant.get_ontology(str(path.joinpath('ontologies','restaurant_model.owl'))).load()
obop_world2 = world_restaurant.get_ontology(str(path.joinpath('ontologies','obop.owl'))).load()
world_test = World()
testing_model = world_test.get_ontology(str(path.joinpath('ontologies','test_model.owl'))).load()
obop_world3 = world_test.get_ontology(str(path.joinpath('ontologies','obop.owl'))).load()

ontology_models = { "flight_world" : {"world": world_flights, "obop" : obop_world1},
                   "basic_model": {"world": world_restaurant, "obop" : obop_world2}, 
                    "test_model" : {"world": world_test, "obop" : obop_world3}}
onto_output = get_ontology(str(path.joinpath('ontologies','output.owl'))).load()

chatbot = ChatBot( name = "Ontochat",
                    logic_adapters=[
                        {
                            'import_path': 'chatterbot.logic.BestMatch',
                        },
                        {
                            'import_path': 'ontoadapter.myadapters.OntoChatterAdapter',
                        },
                       'chatterbot.logic.MathematicalEvaluation',
                       'chatterbot.logic.TimeLogicAdapter'
                    ],
                    database_uri='sqlite:///database.sqlite3',
                    ontology_models = ontology_models, 
                    output_ontology = onto_output,
                )

#corpus_trainer = ChatterBotCorpusTrainer(chatbot)
#corpus_trainer.train("chatterbot.corpus.english")
