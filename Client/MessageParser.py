import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
	    # More key:values pairs are needed	
            'message': self.parse_message,
            'history': self.parse_history
        }

    def parse(self, payload):
        received_json = json.loads(payload)

        if received_json['response'] in self.possible_responses:
            return self.possible_responses[received_json['response']](received_json)
        else:
            # Response not valid
            return

    def parse_error(self, payload):
        print 'Error:  %s' % payload['content']
    
    def parse_info(self, payload):
        print 'Info:  %s' % payload['content']

    def parse_message(self, payload):
        print " %s %s : %s" % (payload['timestamp'], payload['sender'],  payload['content'])

    def parse_history(self, payload):
        #For lokke
        print 'History:'

        for jsonHistory in payload['content']:
            history = json.loads(jsonHistory)
            #history er en struct med timestamp, message.
            self.parse_message(history)

    
    # Include more methods for handling the different responses... 
