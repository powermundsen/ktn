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
        payload = {'request': req, 'content':cont} # decode the JSON object

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            # Response not valid
            return

    def parse_error(self, payload):
        print 'Error:  %s' % payload['content']
    
    def parse_info(self, payload):
        print 'Info:  %s' % payload['content']

    def parse_message(self, payload):
        print '%i %s: %s' % datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), payload['sender'], payload['content']

    def parse_history(self, payload):
        #For lokke
        print 'History:  %s', payload[content]

    
    # Include more methods for handling the different responses... 
