from chatterbot.conversation import Statement
from owlready2 import default_world
from ontoadapter.conversation_state import Conversation_state
from pathlib import Path
import logging
"""
    OntoConversationSingleton is defined as singleton class because it can be only 
    single one for a conversation in order to keep track of the current state of 
    that conversation
"""
class OntoConversationSingleton(object):
    instance = None  
    class __OntoConversation():
        def __init__(self):
            self.state = Conversation_state()

            self.ontology_models = None 
            self.ontologies = None
            self.output_ontology = None 
            self.current_ontology_model = None

            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)

        def search_for_string(self, input_statement, mode) :
            self.state.print_status()
            if mode=='probe' : 
                if input_statement=="":
                    return True 
            if self.state.status == 'waiting_for_model' and self.current_ontology_model is None:
                #chatbot is waiting for a user to choose wanted ontology model (world)
                self.select_ontology_model(input_statement)
            # self.logger.debug(self.ontology_model.imported_ontologies)
            # self.logger.debug('List of individuals: \n')
            # self.logger.debug(list(self.ontology_model.individuals()))
            # Finding the entry element of this conversation block
            if self.state.current_block is None:
                try:
                    self.state.current_block = self.current_ontology_model.search(type = self.ontologies.Block, hasPositionNumber = 1)
                    if self.state.current_block is None:
                        raise Exception (self.current_ontology_model)
                except Exception as no_current_block:
                    self.logger.info("There is no conversational block in the ontology model" + str(self.current_ontology_model) )
            current_conversation_block = self.state.current_block
            # Populating data in the output graph if the chatbot is waiting for a new data
            if self.state.status == "insert" and self.state.model_previous_node is not None: 
                self.insert_data(input_statement)

            return self.take_new_node_and_generate_response(current_conversation_block) 

        def take_new_node_and_generate_response(self, current_conversation_block):
            self.finding_next_node(current_conversation_block)

            # If the current node is of type Field then it requires data to be entered
            if self.state.current_node is not None and self.ontologies.Field in self.state.current_node.is_a :
                output_string = str(self.state.current_node.hasLabel[0])
                self.state.status = "insert"
                self.state.insert_type = "new_instance"
            else:
                output_string = ""

            self.state.model_previous_node = self.state.current_node
            answer = "Insert data for " + str(output_string);
            response_statement = Statement(text = answer)
            response_statement.confidence = 1

            self.print_output_ontology_state()
            return response_statement

        def finding_next_node(self, current_conversation_block):
            if self.state.startnode is None : 
                # Searching for the field that starts the current conversation block
                self.state.startnode = self.current_ontology_model.search_one(type = self.ontologies.Field, 
                                                       hasPositionNumber = 1, 
                                                       belongsTo = current_conversation_block )
                self.state.current_node = self.state.startnode
                self.state.positionNumber = 1
            else:
                self.state.positionNumber += 1
                self.state.current_node = self.current_ontology_model.search_one(type = self.ontologies.Field, 
                                                       hasPositionNumber = self.state.positionNumber, 
                                                        belongsTo = current_conversation_block )

        def insert_data(self, input_statement):
            data_property_name = self.state.model_previous_node.containsDatatype[0] 
            self.state.model_individual_type = self.state.model_previous_node.isRelatedToTargetOntologyInstance[0] 
            # if instance of a class is not already created call the function to create it
            if self.state.output_original_instance is None: 
                self.state.output_original_instance = self.create_original_output_instance(self.state.model_individual_type)
            # insert data property related to the output_original_instance
            self.insert_data_property(input_statement, data_property_name )
            self.state.status = "waiting"
            self.insert_type = ""
            path = Path.cwd()
            self.output_ontology.save(str(path.joinpath('ontologies','output-intermediate.owl')))

        def select_ontology_model(self, input_statement):
            """ 
                According to the input text (containing number) current_ontology_model should be 
                selected from the dctionary of all ontology models
            """
            import re
            self.logger.debug("waiting: Input statement:")
            self.logger.debug(input_statement.__dict__)
            self.logger.debug("Chosen_option " + input_statement.text)
            chosen_option = re.findall('\-?\d+', input_statement.text)
            self.logger.debug("Chosen option is: " + chosen_option[0])
            for onto_world in self.ontology_models.values(): 
                if chosen_option[0] == str(onto_world['index']):
                    self.ontologies = onto_world.get("obop") 
                    self.current_ontology_model = onto_world.get('world')


        


        def create_original_output_instance(self, model_individual_type):
            """ 
                Creating a new individual (instance) that belongs to classes of the target ontologies.
                which is already described in the individual of the model. 
                Parameter model_individual type contains now the list of classes that this individual 
                is instance of.
            """
            new_target_ontologies_instance = None
            with self.output_ontology: 
               for index, item in enumerate(model_individual_type.is_a):
                   if index == 0: 
                       new_target_ontologies_instance = item() 
                   else:
                       new_target_ontologies_instance.is_a.append(item)
            print('New instance in the function is:', end = '')
            print(new_target_ontologies_instance.iri)
            return new_target_ontologies_instance

             

        def insert_data_property(self, text, data_property_name):
            #current_place_holder = find_current_instance() 
            if self.state.insert_type == "new_instance" and self.state.model_previous_node is not None: 
                print('Insert data property for the model: ', end='')
                print(self.state.model_previous_node)
                print('Insert data property for the instance: ', end='')
                print(self.state.output_original_instance)               
                with self.output_ontology:
                    if data_property_name.is_functional_for(self.create_original_output_instance.__class__) :
                        setattr(self.state.output_original_instance, str(data_property_name.name), str(text))
                    else :
                        getattr(self.state.output_original_instance, str(data_property_name.name)).append(str(text))

        def print_output_ontology_state(self):
            print("Output ontology state:")
            print ("\nList of the output knowledge graph classes :", end='')
            for c in self.output_ontology.classes(): print (c.name)
            #print(BusinessEntity)
            print ("List of oputput ontology individuals:")
            for i in self.output_ontology.individuals(): print(i) 


        def list_ontology_models(self, ontology_models):
            """
               List all model descriptions to ask 
               what ontology would be suitable for the user. 
            """  
            output_text = "Please choose one of the following tasks: "

            if len(ontology_models) > 0 :
                for index, ontology_world in enumerate(ontology_models.values()): 
                    #for i in ontology_world.get("world").individuals(): print(i)
                    # OBOP ontology in loaded from the dictionary 
                    self.ontologies = ontology_world.get("obop") 
                    model_individual = ontology_world.get("world").search_one(type = self.ontologies.Model)
                    output_text += "\n" + str(index + 1) + ": " + str( model_individual.modelDescription[0])
                    ontology_world["index"] = index + 1

                output_text += "\n Enter a corresponding number for a wanted option:"
                self.ontology_models = ontology_models
                self.state.status = 'waiting_for_model'

            else: 
                    output_text = "There is no input model."

            response_statement = Statement( text = output_text)
            response_statement.confidence = 1
            return  response_statement

    def __new__(cls):
        if not OntoConversationSingleton.instance:
            OntoConversationSingleton.instance = OntoConversationSingleton.__OntoConversation()
        return OntoConversationSingleton.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)
       
    def __setattr__(self, name):
        return setattr(self.instance, name)

    def search_for_string(self, text):
        return self.instance.search_for_string(text, "probe")

    def selected_statement(self, text):
        return self.instance.search_for_string(text, "data")


