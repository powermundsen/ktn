# -*- coding: utf-8 -*-

"""
This is the ClientHandler class. Everytime a new client connects to the
server, a new ClientHandler object will be created. This class represents
only connected clients, and not the server itself. If you want to write
logic for the server, you must write it outside this class.
"""

import SocketServer
import datetime
import json
import re
import socket
import errno  


connectedClients = []   #List of connected clients
history = []            #List of chat history
taken_usernames = []    #List of used usernames

class ClientHandler(SocketServer.BaseRequestHandler):
    username = ""

    #Method for handeling the connection between a client and the server.
    def handle(self):
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request 

        # Loop that listens for messages from the client
        while True:
            try:
                received_string = self.connection.recv(1024) 
                received_json = json.loads(received_string)

                if received_json['request'] == 'login':
                    self.login(received_json['content'])


                elif received_json['request'] == 'help':
                    self.help()
                

                elif received_json['request'] == 'logout': 
                    if self.username == '':
                        raise Exception('Not logged in')   
                    self.logout()


                elif received_json['request'] == 'msg':
                    if self.username == '':
                        raise Exception('Not logged in') 
                    self.msg(received_json['content'])


                elif received_json['request'] == 'names':
                    if self.username == '':
                        raise Exception('Not logged in') 
                    self.names()
                else:
                    self.help()


            except socket.error as error:
                if self.username != "":
                    if self in connectedClients:
                        connectedClients.remove(self)
                    if self.username in taken_usernames:
                        print 'I remove username when interrupted'
                        taken_usernames.remove(self.username)
            except Exception, e:
                payload = json.dumps({'timestamp': datetime.datetime.now().strftime("%H:%M %d.%m.%y"), 'sender': 'server', 'response': 'error', 'content': str(e)})
                self.connection.send(payload)


    def login(self, username):

        if re.match("^[A-Za-z0-9]*$", username):
            if username not in taken_usernames:
                self.username = username
                connectedClients.append(self)
                taken_usernames.append(self.username)
                print 'New user %s connected' % self.username

                payload = json.dumps({'timestamp': datetime.datetime.now().strftime("%H:%M %d.%m.%y"), 'sender': 'server', 'response': 'info', 'content': 'Login successful, great to have you here %s!' % self.username})
                self.connection.send(payload)
                if history != []:
                    payload = json.dumps({'timestamp': datetime.datetime.now().strftime("%H:%M %d.%m.%y"), 'sender': 'server', 'response': 'history', 'content': history})
                    self.connection.send(payload)

            else:
                raise Exception("Username taken, try another please")
        else:
            raise Exception('Username unvalid. Try another username with the allowed characters: A-Z, a-z, 0-9')

    def logout(self):
        try: 

            #Remove from the active connections
            if self in connectedClients:
                connectedClients.remove(self)
            if self.username in taken_usernames:
                taken_usernames.remove(self.username)

            payload = json.dumps({'timestamp': datetime.datetime.now().strftime("%H:%M %d.%m.%y"), 'sender': 'server', 'response': 'info', 'content': 'You are now logged out \n Have a nice day! :-)'})
            self.connection.send(payload)


            #Alerting all users
            payload = json.dumps({'timestamp': datetime.datetime.now().strftime("%H:%M %d.%m.%y"), 'sender': 'server', 'response': 'info', 'content': 'User: %s has logged out' % self.username})
            for client in connectedClients:
                client.connection.send(payload)

            self.username = ''
            print 'User: %s has logged out' % self.username #Kan man aksessere self.username når har closed?
            #self.connection.close()

        except:
            raise Exception('Logout failed.')

    def msg(self, msg):
        #Send beskjed på chat med timestamp
        try:
            payload = json.dumps({'timestamp': datetime.datetime.now().strftime("%H:%M %d.%m.%y"), 'sender': self.username, 'response': 'message', 'content': msg})
            print "Legger til i history"
            history.append(payload)
            print "Lagt til i history"

            for client in connectedClients:
                client.connection.send(payload)
        except:
            raise Exception('Message sending failed.')

    def names(self):
        try: 
            names = ''
            for taken_username in taken_usernames:
                names += taken_username + ", "
            payload = json.dumps({'timestamp': datetime.datetime.now().strftime("%H:%M %d.%m.%y"), 'sender': "Server", 'response': 'info' ,'content': 'The connected users are: ' + names})
            self.connection.send(payload)
        except:
            raise Exception('Retrieving names failed.')

    def help(self):
        try:
            helpMessage = '\n \nThe allowed commands are as follows:\nlogin <username> : To join in to the chat\nlogout: To leave the chat\nmsg <message>: Send a message to the connected chatters\nnames: Get a list of all connected chatters\nhelp: Get a list like this one'
            payload = json.dumps({'timestamp': datetime.datetime.now().strftime("%H:%M %d.%m.%y"), 'sender': "Server", 'response': 'info' ,'content': helpMessage})
            self.connection.send(payload)
        except:
            raise Exception('Retrieving info failed.')




class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
