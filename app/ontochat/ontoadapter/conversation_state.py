import logging

class Conversation_state():
    def __init__(self):
        self._status = None
        self.model_previous_node = None
        self.output_original_instance = None
        self.startnode = None
        self.insert_type = None
        self.positionNumber = None
        self.active_instance = None
        self.current_block = None
        self.current_node = None

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, s): 
        self._status = s;

    def print_status(self):
        self.logger.debug("Status: " + 
            self._status if self._status else "") 

        self.logger.debug("Previous node : " + self.model_previous_node.iri 
                if self.model_previous_node and self.model_previous_node.iri 
                else "")
        self.logger.debug("Start node: " + self.startnode.iri 
                if self.startnode and self.startnode.iri else "")
        self.logger.debug("Type of insert: " + self.insert_type 
                if self.insert_type else "")
        self.logger.debug("Position number: " + str(self.positionNumber)
                if self.positionNumber else "")
        self.logger.debug("Active instance: " + str(self.active_instance) 
                if self.active_instance else "")
        self.logger.debug("Current block: " + str(self.current_block) 
                if self.current_block else  "")
        self.logger.debug("Current node : " + self.current_node.iri 
                if self.current_node and self.current_node.iri 
                else "")
        self.logger.debug("Original instance: " + self.output_original_instance.iri 
                if self.output_original_instance and self.output_original_instance.iri 
                else  "")