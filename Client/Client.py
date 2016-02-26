# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import json
import os   

class Client:
    def __init__(self, host, server_port):

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.server_port = server_port
        self.run()
        self.msg = ''

    def run(self):


        # Connecting to server
        self.connection.connect((self.host, self.server_port))

        #Creats the running thread for recieving messages 
        self.thread = MessageReceiver(self, self.connection)
        self.thread.start()  #--> run in MessageReceiver
        running_status = self.thread.is_alive()

        while running_status:

            #Collects input from chat-user
            user_input = raw_input().split(' ', 1 )
            request = user_input[0]
            content = 'None'

            try:
                content = user_input[1]
            except Exception, e:
                pass


            if request == 'login':
                try:
                    content = user_input[1]
                except Exception, e:
                    print '[ERROR] Username unvalid. Try another username with the allowed characters: A-Z, a-z, 0-9'
                    pass

                payload = json.dumps({'request': 'login', 'content': content})
                self.send_payload(payload)

            elif request == 'logout':
                payload = json.dumps({'request': 'logout', content: None})
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
                payload = json.dumps({'request': 'help', 'content': None})
                self.send_payload(payload)
        pass

        
    def disconnect(self):
        self.connection.close()
        self.thread.is_alive = False
        print "Connction to server terminatet by user"
        pass

    def receive_message(self, message):
        message_parser = MessageParser()
        message_parser.parse(message)
        pass

    def send_payload(self, data):
        self.connection.send(data)
        pass


if __name__ == '__main__':
    #Clear terminal window 
    os.system('cls' if os.name == 'nt' else 'clear')
    print '\
                    ──────▄▀▀▄────────────────▄▀▀▄────\n\
                    ─────▐▒▒▒▒▌──────────────▌▒▒▒▒▌───\n\
                    ─────▌▒▒▒▒▐─────────────▐▒▒▒▒▒▐───\n\
                    ────▐▒▒▒▒▒▒▌─▄▄▄▀▀▀▀▄▄▄─▌▒▒▒▒▒▒▌──\n\
                    ───▄▌▒▒▒▒▒▒▒▀▒▒▒▒▒▒▒▒▒▒▀▒▒▒▒▒▒▐───\n\
                    ─▄▀▒▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌───\n\
                    ▐▒▒▒▌▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐───\n\
                    ▌▒▒▌▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌──\n\
                    ▒▒▐▒▒▒▒▒▒▒▒▒▄▀▀▀▀▄▒▒▒▒▒▄▀▀▀▀▄▒▒▐──\n\
                    ▒▒▌▒▒▒▒▒▒▒▒▐▌─▄▄─▐▌▒▒▒▐▌─▄▄─▐▌▒▒▌─\n\
                    ▒▐▒▒▒▒▒▒▒▒▒▐▌▐█▄▌▐▌▒▒▒▐▌▐█▄▌▐▌▒▒▐─\n\
                    ▒▌▒▒▒▒▒▒▒▒▒▐▌─▀▀─▐▌▒▒▒▐▌─▀▀─▐▌▒▒▒▌\n\
                    ▒▌▒▒▒▒▒▒▒▒▒▒▀▄▄▄▄▀▒▒▒▒▒▀▄▄▄▄▀▒▒▒▒▐\n\
                    ▒▌▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▄▄▄▒▒▒▒▒▒▒▒▒▒▒▐\n\
                    ▒▌▒▒▒▒▒▒▒▒▒▒▒▒▀▒▀▒▒▒▀▒▒▒▀▒▀▒▒▒▒▒▒▐\n\
                    ▒▌▒▒▒▒▒▒▒▒▒▒▒▒▒▀▒▒▒▄▀▄▒▒▒▀▒▒▒▒▒▒▒▐\n\
                    ▒▐▒▒▒▒▒▒▒▒▒▒▀▄▒▒▒▄▀▒▒▒▀▄▒▒▒▄▀▒▒▒▒▐\n\
                    ▒▓▌▒▒▒▒▒▒▒▒▒▒▒▀▀▀▒▒▒▒▒▒▒▀▀▀▒▒▒▒▒▒▐\n\
                    ▒▓▓▌▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌\n\
                    ▒▒▓▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌─\n\
                    ▒▒▓▓▀▀▄▄▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐──\n\
                    ▒▒▒▓▓▓▓▓▀▀▄▄▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▄▄▀▀▒▌─\n\
                    ▒▒▒▒▒▓▓▓▓▓▓▓▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▒▒▒▒▒▐─\n\
                    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌\n\
                    ▒▒▒▒▒▒▒█▒█▒█▀▒█▀█▒█▒▒▒█▒█▒█▒▒▒▒▒▒▐\n\
                    ▒▒▒▒▒▒▒█▀█▒█▀▒█▄█▒▀█▒█▀▒▀▀█▒▒▒▒▒▒▐\n\
                    ▒▒▒▒▒▒▒▀▒▀▒▀▀▒▀▒▀▒▒▒▀▒▒▒▀▀▀▒▒▒▒▒▒▐\n\
                    █▀▄▒█▀▄▒█▀▒█▀█▒▀█▀▒█▒█▒█▒█▄▒█▒▄▀▀▐\n\
                    █▀▄▒█▀▄▒█▀▒█▄█▒▒█▒▒█▀█▒█▒█▀██▒█▒█▐\n\
                    ▀▀▒▒▀▒▀▒▀▀▒▀▒▀▒▒▀▒▒▀▒▀▒▀▒▀▒▒▀▒▒▀▀▐\n\
                    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐'


    print "\n                ~~~~~~~ Welcome to this awesome chat! ~~~~~~~\n            ~~~~~~~Type 'login' and then your username to begin~~~~~~~ \n \n"
    client = Client('localhost', 9998)

    #bare endre lokalhost til IP-adresse til PC!



