from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from owlready2 import JAVA_EXE
from owlready2 import sync_reasoner
from ontoadapter.onto_conversation import OntoConversationSingleton  
JAVA_EXE = 'usr/bin/java'

#The following lines were necessary to import our  
# ontology based logical adapter from the current path
import os.path
import sys
current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_directory)

class OntoChatterAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        self.ontologies = kwargs.get('ontologies')
        self.ontology_models = kwargs.get('ontology_models')
        self.output_ontology = kwargs.get('output_ontology')
        self.ontochatConversation = OntoConversationSingleton() 
        print("----------------------\n" + "Creating OntoChatterAdapter")
        self.ontochatConversation.ontologies = self.ontologies
        self.ontochatConversation.current_ontology_model = None 
        self.ontochatConversation.output_ontology = self.output_ontology


    def can_process(self, statement):
        """
            can_process() function gives an answer as to what ontology_model among those 
            given in the ontology_models dictionary could be used to model conversation
            to populate the domain graph. If such a model does not exist then the function
            returns False
            @ statement: if statement.text is an empty string then the function should 
              return question to ask which model the user wants to use with the list of 
              those questions   
        """       
        if self.ontochatConversation.current_ontology_model is None :
            if statement.text == "":
               return True;
            else: 
                return False
        else:
            return self.ontochatConversation.search_for_string(statement.text, "probe")
         
    def process(self, input_statement, additional_response_selection_parameters):
        """
        This function returns a response using ontochatbot 
        Args:
            input_statement (_type_): it contains the input string
              if  the input_statement.text is an empty string then the function should 
              return question to ask which model the user wants to use. The question 
              returns a list of those questions:
 

            additional_response_selection_parameters (_type_): _description_

        Returns:
            _type_: _description_
        
        """
        # if the function gets an empty string while current_ontology_model is not yet
        # chosen then it returns the list
        # the user hast to select on option from the list 
        if self.ontochatConversation.current_ontology_model is None :
            if input_statement.text == "":
                for ontology_model in self.ontology_models.values(): 
                    response_statement = self.ontochatConversation.list_ontology_models(input_statement.text, ontology_model)
                    response_statement.confidence = 1
                    return response_statement
        else: 
            response_statement = self.ontochatConversation.search_for_string(input_statement, "data")
        return response_statement



