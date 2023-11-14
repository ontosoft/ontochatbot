import logging

class Conversation_state():
    def __init__(self):
        self._activity = None
        # activity specifies what process is active combined with other status fields
        # activity == "insert" - the string entered in the chatbot prompt should be now 
        #      saved in the knowledge graph
        # acitivity == "branching" - string is already inserted and the system should move 
        #      to the next node in the model knowledge graph  

        self.activity_status = None
        # activity_status is combined together with the activity member and there exits
        # different statuses depending on the sort of activity
        # activity_status == "speaking_to_user" - if the activity is "insert" then 
        #     the system read what should be done and answers back to the user 
        # activity_status == "waiting" - if the activity is "insert" then the user gave data 
        #     and the system 
        #     yet to be created 
        # new individual should be created
        # activity_status ==  "done" # if the activity is, for example, is insert this means
        #     that the string is already inserted and the system should move to the next 
        #     node in the model knowledge graph

        self.output_instance_status = None 
        # output_instance_status is combined together with other status members. It
        # specifies if the output instance is already created
        # output_instance_status == "no_instance" - then a new instance (individual) has 
        #     yet to be created 
        # output_instance_status ==  "instance_exists" it means that new data should be inserted as
        #     data property of that existing instance (individual) which is stored in 
        #     the class member called output_active_instance
        self.current_block = None
        self.startnode = None
        self.model_current_node = None
        self.model_previous_node = None
        self.positionNumber = None
        self.output_active_instance = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    @property
    def activity(self):
        return self._activity

    @activity.setter
    def activity(self, s): 
        self._activity = s;

    def print_status(self):
        self.logger.debug("Activity : " + 
            self.activity if self.activity else "") 
        self.logger.debug("Activity status: " + self.activity_status 
                if self.activity_status else "")
        self.logger.debug("Previous node : ") 
        self.logger.debug(self.model_previous_node.iri 
                          if self.model_previous_node and self.model_previous_node.iri else "")
        self.logger.debug("Current block: " + str(self.current_block) 
                if self.current_block else  "")
        self.logger.debug("Current node : " + self.model_current_node.iri 
                if self.model_current_node and self.model_current_node.iri 
                else "")
        self.logger.debug("Start node: " + self.startnode.iri 
                if self.startnode and self.startnode.iri else "")
        self.logger.debug("Position number: " + str(self.positionNumber)
                if self.positionNumber else "")
        self.logger.debug(" Output active instance: " + str(self.output_active_instance) 
                if self.output_active_instance else "")
