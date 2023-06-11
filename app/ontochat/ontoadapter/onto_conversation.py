from chatterbot.conversation import Statement
from owlready2 import default_world
from pathlib import Path
"""
    OntoConversationSingleton is defined as singleton class because it can be only 
    single one for a conversation in order to keep track of the current state of 
    that conversation
"""
class OntoConversationSingleton(object):
    instance = None  
    class __OntoConversation():
        def __init__(self):
            self.ontology_model = None 
            self.ontologies = None
            self.output_ontology = None 
            self.current_ontology_model = None

            self.status = None
            self.model_previous_node = None
            self.output_original_instance = None
            self.startnode = None
            self.insert_type = None
            self.positionNumber = None
            self.active_instance = None
            self.current_block = None
        
        def search_for_string(self, text, status):
            self.print_status()
            if status=='probe' : 
                if text=="":
                    return True 
            # print(self.ontology_model.imported_ontologies)
            # print('List of individuals: \n')
            # print(list(self.ontology_model.individuals()))
            # Finding the entry element of this conversation block
            if self.current_block is None:
                self.current_block = self.ontology_model.search(type = self.ontologies.Block, hasPositionNumber = 1)
            current_conversation_block = self.current_block
            # Populating data in the output graph if the chatbot is waiting for a new data
            if self.status == "insert" and self.model_previous_node is not None: 
                data_property_name = self.model_previous_node.containsDatatype[0] 
                self.model_individual_type = self.model_previous_node.isRelatedToTargetOntologyInstance[0] 
                if self.output_original_instance is None: 
                    self.output_original_instance = self.create_original_output_instance(self.model_individual_type)
                self.insert_data_property(text, data_property_name )
                self.status = "waiting"
                self.insert_type = ""
                path = Path.cwd()
                self.output_ontology.save(str(path.joinpath('ontologies','output-intermediate.owl')))

            if self.startnode == None : 
                # Searching for the field that starts the current conversation block
                self.startnode = self.ontology_model.search_one(type = self.ontologies.Field, 
                                                       hasPositionNumber = 1, 
                                                       belongsTo = current_conversation_block )
                self.current_node = self.startnode
                self.positionNumber = 1
            else:
                self.positionNumber += 1
                self.current_node = self.ontology_model.search_one(type = self.ontologies.Field, 
                                                       hasPositionNumber = self.positionNumber, 
                                                        belongsTo = current_conversation_block )

            # If the current node is of type Field then it requires data to be entered
            if self.current_node is not None and self.ontologies.Field in self.current_node.is_a :
                output_string = str(self.current_node.hasLabel[0])
                self.status = "insert"
                self.insert_type = "new_instance"
            else:
                output_string = ""

            self.model_previous_node = self.current_node
            answer = "Insert data for " + str(output_string);
            response_statement = Statement(text = answer)
            response_statement.confidence = 1

            self.print_ontology_state()
            return response_statement 




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
            if self.insert_type == "new_instance" and self.model_previous_node is not None: 
                print('Insert data property for the model: ', end='')
                print(self.model_previous_node)
                print('Insert data property for the instance: ', end='')
                print(self.output_original_instance)               
                with self.output_ontology:
                    setattr(self.output_original_instance, str(data_property_name.name), str(text))

        def print_ontology_state(self):
            print("Ontology state:")
            print ("\nList of classes :", end='')
            for c in self.output_ontology.classes(): print (c.name)
            #print(BusinessEntity)
            print ("List of individuals:")
            for i in self.output_ontology.individuals(): print(i) 


        def list_ontology_model(self, text, ontology_models):
            found = onto.search_one(label = text)
            # if the text is empty string then we assign the current ontology to the
            # current_ontology_model. 

            self.ontology_models  = ontology_models;
            if found or text =="":
                text = "Please choose one of the given tasks:"
                for ontology_model in self.ontology_models.values(): 
                    text = ontology_model.search_one(label = text) 
                    response_statement = Statement(
                        text = self.ontochatConversation.list_ontology_models(
                            input_statement.text, ontology_model))
                    response_statement.confidence = 1


        def print_status(self):
            print("\n-------------------------------\n")
            print("Status: ", end='') 
            print(self.status) if self.status else print("")
            print("Previous node : ", end='' )
            print(self.model_previous_node.iri) if self.model_previous_node and self.model_previous_node.iri else print("")
            print("Start node: ", end='' ) 
            print(self.startnode.iri) if self.startnode and self.startnode.iri else print("")
            print("Type of insert: ", end='')
            print(self.insert_type) if self.insert_type else print("")
            print("Position number: ", end='' )
            print(self.positionNumber) if self.positionNumber else print("")
            print("Active instance: ", end='')
            print(self.active_instance) if self.active_instance else print("")
            print("Current block: ", end='')
            print(self.current_block) if self.current_block else print("")
            print("Original instance: ", end='')
            print(self.output_original_instance.iri) if self.output_original_instance and self.output_original_instance.iri else print("")
    
            




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


