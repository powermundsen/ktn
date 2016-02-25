# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import json

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # TODO: Finish init process with necessary code
        self.host = host
        self.server_port = server_port
        self.run()
        self.msg = ''

    def run(self):
        # Kobler til server
        self.connection.connect((self.host, self.server_port))

        #Lager en traad å kjore paa 
        self.thread = MessageReceiver(self, self.connection)
        #Kjorer traaden
        self.thread.start()

        running_status = self.thread.is_alive()

        while running_status:

            #Hent input fra bruker
            user_input = raw_input().split(' ', 1 )
            print "Melding fra bruker mottatt "
            #Sorter keyword og innhold, takler kun 'help', 'names'
            request = user_input[0]
            content = 'None'
            try:
                content = user_input[1]
            except Exception, e:
                pass
            print "Formatert melding "

            if request == 'login':
                print "Login mottatt"
                payload = json.dumps({'request': 'login', 'content': content})
                print "Pakket som json"
                self.send_payload(payload)
                print "Sendt med self.send_payload(payload)"

            elif request == 'logout':
                payload = json.dumps({'request': 'logout'})
                self.send_payload(payload)

            elif request == 'msg':
                payload = json.dumps({'request': 'msg', 'content': content})
                self.send_payload(payload)

            elif request == 'names':
                payload = json.dumps({'request': 'names', 'content': None})
                self.send_payload(payload)

            elif request == 'help':
                payload = json.dumps({'request': 'help', 'content': None})
                self.send_payload(payload)

            else:
                print "Hva er det du prover paa? "
                return
        pass

        
    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.close()
        self.thread.is_alive = False
        print "Connction to server terminatet by user"
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message

        message_parser = MessageParser()
        message_parser.parse(message)



        # try:
        #     message = json.loads(message)
        #     pass
        # except Exception, e:
        #     return

        # if message['response'] == 'msg':
        #     print message['timestamp'], message['sender'] + ':',  message['content']

        # elif message['response'] == 'info':
        #     print message['timestamp'] + 'INFO' + ':', message['content']
        


        pass

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        self.connection.send(data)
        pass
        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """

    print "Welcome to this chat! Type login and your username to begin"
    client = Client('localhost', 9998)

