from chatterbot.conversation import Statement
from ontoadapter.conversation_state import Conversation_state
from pathlib import Path
from owlready2 import get_ontology, World
from owlready2 import default_world
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

        """
                   """
        def search_for_string(self, input_statement, mode) :
            """
                This function is called by an ontochat adapter. It is the entry point for 
                communication with our chatbot. 
                
            Args:
                input_statement ( string): _description_
                mode (string): _description_
                if mode == "probe" then 
                    the system is testing whether this adapter can answer to that question
                if mode == "data" then 
                    the system processes the request - for instance, inserts data 

            Raises:
                Exception: _description_

            Returns:
                _type_: _description_
            """
            self.state.print_status()
            if mode=='probe' : 
                if input_statement=="":
                    return True 
            else:
                if self.state.activity == 'waiting_for_model' and self.current_ontology_model is None:
                    #chatbot is waiting for a user to choose wanted ontology model (world)
                    self.select_ontology_model(input_statement)
                # self.logger.debug(self.ontology_model.imported_ontologies)
                # self.logger.debug('List of individuals: \n')
                # self.logger.debug(list(self.ontology_model.individuals()))
                if self.state.current_block is None:
                    try:
                        # Finding the entry element of this conversation block
                        self.state.current_block = self.current_ontology_model.search(type = self.ontologies.Block, hasPositionNumber = 1)
                        if self.state.current_block is None:
                            raise Exception (self.current_ontology_model)
                        else:
                            # Now the system has a model and the activity is beginning
                            self.state.activity == "beginning"
                    except Exception as no_current_block:
                        self.logger.info("There is no conversational block in the ontology model" + str(self.current_ontology_model) )
                current_conversation_block = self.state.current_block
                # Populating data in the output graph if the chatbot is waiting for a new data
                if self.state.activity == "insert":  
                    self.insert_data(input_statement)

                return self.take_new_node_and_generate_response(current_conversation_block) 

        def take_new_node_and_generate_response(self, current_conversation_block):
            """ 
            This function goes further through the model to generate new question or 
            ansewer the user 

            Args:
                current_conversation_block (_type_): _description_

            Returns:
                _type_: _description_
            """            
            self.finding_next_node(current_conversation_block)

            # If the current node is of type "Question" then it requires data to be entered
            if self.state.model_current_node is not None and self.ontologies.Question in self.state.model_current_node.is_a :
                output_string = str(self.state.model_current_node.hasLabel[0])
                self.state.activity = "insert"
                self.state.activity_status = "waiting" # the system is waiting on end-user responce


            else:
                output_string = ""

            answer = str(output_string);
            response_statement = Statement(text = answer)
            response_statement.confidence = 1

            self.print_output_ontology_state()
            return response_statement

        def finding_next_node(self, current_conversation_block):
            """ Finding the next node - it can be in the same block or in the next block 
                following the structure of a connection element
                This updates the variable self.state.current_node to a new value

            Args:
                current_conversation_block (_type_): _description_
            """
            if self.state.startnode is None : 
                # Searching for the question that starts the current conversation block
                self.state.startnode = self.current_ontology_model.search_one(type = self.ontologies.Question, 
                                                       hasPositionNumber = 1, 
                                                       belongsTo = current_conversation_block )
                self.state.model_current_node = self.state.startnode
                self.state.positionNumber = 1
            else:
                self.state.positionNumber += 1
                next_node_in_the_same_block = self.current_ontology_model.search_one(type = self.ontologies.Question, 
                                                       hasPositionNumber = self.state.positionNumber, 
                                                        belongsTo = current_conversation_block )
                if next_node_in_the_same_block is not None: 
                    self.state.model_previous_node = self.state.model_current_node
                    self.state.model_current_node = next_node_in_the_same_block  
                else: 
                    # TODO: search for a possible connection element
                    # or end of the conversation
                    pass

        def insert_data(self, input_statement):
            # The current activity is insert
            if self.state.model_current_node.isRelatedToTargetOntologyInstance is not None:
                model_individual_types = self.state.model_current_node.isRelatedToTargetOntologyInstance[0] 
            specified_iri = self.state.model_current_node.specifiesEndOfIRI
            specified_dataproperty = self.state.model_current_node.containsDatatype

            if self.state.activity_status=="waiting":
                #Checking out whether the inserted string should be added as the ending of the IRI or 
                # as a data property 
                if specified_iri is not None and specified_iri:
                    # if an instance of class is still not created - call the function to create it
                    # with the specified string as the end of iri
                    if self.state.output_instance_status == "no_instance" and self.state.output_active_instance is None : 
                        self.state.output_active_instance = self.create_original_output_instance(
                            model_individual_types, specified_iri, input_statement)
                        self.state.output_insert_status = "instance_exists"
                elif specified_dataproperty is not None and specified_dataproperty[0]:
                    # if an instance of class is still not created - call the function to create it
                    # with an automatically generated iri 
                    if self.state.output_instance_status == "no_instance" and self.state.output_active_instance is None : 
                        self.state.output_active_instance = self.create_original_output_instance( 
                            model_individual_types, None, None)
                        self.state.output_insert_status = "instance_exists"
                    data_property_name = specified_dataproperty[0] 
                    # insert data property related to the output_original_instance
                    self.insert_data_property(input_statement, data_property_name )
                self.state.activity_status = "done"
            # Here should be distinguished waiting for the new data and waiting after some 
            # data are inserted and now n
            # When the status of the node is "waiting" then it should be found a new model 
            # node what is done with 
            path = Path.cwd()
            if self.output_ontology:
                print("Insert is done")
                print(self.output_ontology.imported_ontologies)
                self.output_ontology.save(str(path.joinpath('ontologies','output-intermediate.owl')))
            self.print_output_ontology_state()

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
                    self.output_ontology=default_world.get_ontology("http://example.org/ontochatbot")

        def create_original_output_instance(self, model_individual_types, iri, iri_ending):
            """
                Creating a new individual (instance) that belongs to classes of the target ontologies.
                which is already described in the individual of the model. 
                Parameter model_individual type contains now the list of classes that this individual 
                is instance of.

             Args:
                model_individual_types (array): array of classes for a new instance 
                iri (bool):  if iri true then that string is added at the
                    end of iri 
                iri_ending (string):  this string is added at the end of iri 

            Returns:
                new_target_ontologies_instance: - a new individual which is an instance 
                of all classes which are specified in the array  

            """
            new_target_ontologies_instance = None
            with self.output_ontology: 
               for index, item in enumerate(model_individual_types.is_a):
                   if index == 0: 
                        # If iri is specified then it is included in the name, otherwise 
                        # it it is automaticaly generated
                        # TODO: it should be considered adding an information according to which model
                        # this instance is generated as specifiec data property for instance
                        if iri:
                            new_target_ontologies_instance = item(iri_ending) 
                        else:
                            new_target_ontologies_instance = item() 
                   else:
                       new_target_ontologies_instance.is_a.append(item)
            self.logger.info('New individual created:')
            self.logger.info(new_target_ontologies_instance.iri)
            return new_target_ontologies_instance

             

        def insert_data_property(self, text, data_property_name):
            #current_place_holder = find_current_instance() 
            if self.state.insert_status == "new_instance" and self.state.model_previous_node is not None: 
                self.state.logger.info('Insert data property for the model: ')
                self.state.logger.info(self.state.model_previous_node)
                self.state.logger.info('Insert data property for the instance: ')
                self.state.logger.info(self.state.output_active_instance)               
                with self.output_ontology:
                    if data_property_name.is_functional_for(self.create_original_output_instance.__class__) :
                        setattr(self.state.output_active_instance, str(data_property_name.name), str(text))
                    else :
                        getattr(self.state.output_active_instance, str(data_property_name.name)).append(str(text))

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
            output_text = "Please choose one of the following tasks: \n"

            if len(ontology_models) > 0 :
                for index, ontology_world in enumerate(ontology_models.values()): 
                    #for i in ontology_world.get("world").individuals(): print(i)
                    # OBOP ontology in loaded from the dictionary 
                    self.ontologies = ontology_world.get("obop") 
                    model_individual = ontology_world.get("world").search_one(type = self.ontologies.Model)
                    output_text += "\n" + str(index + 1) + ": " + str( model_individual.modelDescription[0])
                    ontology_world["index"] = index + 1

                output_text += "\n\n Enter a corresponding number for a wanted option:"
                self.ontology_models = ontology_models
                self.state.activity = 'waiting_for_model'

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


