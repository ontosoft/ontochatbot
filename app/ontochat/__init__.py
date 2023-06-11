from chatterbot import ChatBot
#from chatterbot.trainers import ListTrainer
#from chatterbot.trainers import ChatterBotCorpusTrainer
from . import ontoadapter
from owlready2 import get_ontology
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
onto = get_ontology(str(path.joinpath('ontologies','obop.owl'))).load()
onto_inferences = get_ontology('http://example.com/obop_inferences.owl')
onto_model = get_ontology(str(path.joinpath('ontologies','chat_model.owl'))).load()
onto_model_flights = get_ontology(str(path.joinpath('ontologies','chat_model_flights.owl'))).load()
ontology_models = { "basic_model": onto_model, 
               "flight_model" : onto_model_flights}
onto_output = get_ontology(str(path.joinpath('ontologies','output.owl'))).load()

chatbot = ChatBot( name = "Ontochat",
                    logic_adapters=[
                        'chatterbot.logic.MathematicalEvaluation',                    
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
                    ontologies = onto, 
                    ontology_models = ontology_models, 
                    output_ontology = onto_output,
                )

#corpus_trainer = ChatterBotCorpusTrainer(chatbot)
#corpus_trainer.train("chatterbot.corpus.english")
