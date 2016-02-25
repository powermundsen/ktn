# -*- coding: utf-8 -*-
import SocketServer
import datetime
import json
import re

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

connectedClients = []   #Liste over tilkoblede klienter
history = []            #Dict over historikk, sorteres på key som er timestamp
taken_usernames = []    #Liste over usernames i bruk

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class.
    """

    username = ""

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        connectedClients.append(self)  #Legger til seg selv (connection) til listen over tilkoblede klienter

        # Loop that listens for messages from the client
        while True:
            try:
                #Fra send i client, jeg sender til message receiver
                received_string = self.connection.recv(1024) 
                received_json = json.loads(received_string)
                # TODO: Add handling of received payload from client

                if received_json['request'] == 'login':
                    print 'Gikk inn i login tilfellet'
                    self.login(received_json['content'])
                    print 'sendt til login funksjon'

                elif received_json['request'] == 'help':
                    self.help()
                
                elif received_json['request'] == 'logout': 
                    print 'Logout acked'
                    if self.username == '':
                        raise Exception('Not logged in')   
                    self.logout()

                elif received_json['request'] == 'msg':
                    if self.username == '':
                        raise Exception('Not logged in') 
                    print 'Gikk inn i msg tilfellet'
                    self.msg(received_json['content'])
                    print 'sendt til msg funksjon'

                elif received_json['request'] == 'names':
                    if self.username == '':
                        raise Exception('Not logged in') 
                    self.names()
                else:
                    self.help()

            except Exception, e:
                payload = json.dumps({'timestamp': datetime.datetime.now().strftime("%H:%M %d.%m.%y"), 'sender': 'server', 'response': 'error', 'content': str(e)})
                self.connection.send(payload)


    def login(self, username):  #Skal sjekke om brukernavn er tatt, log inn hvis ja, send feilmelding om nei
        #Sjekk om brukernavn er gyldig formatert
        #Sjekk om brukernavn er tatt fra før
        #Legg til brukernavn med de andre
        if re.match("^[A-Za-z0-9]*$", username):
            print 'Sjekker om brukernavn i taken_usernames'
            if username not in taken_usernames:
                print 'Brukernavn er ikke i taken_usernames'
                self.username = username
                taken_usernames.append(self.username)
                print 'New user %s connected' % self.username
            #uppercase etc and right error &&& send history!!!
                
                info = 'Login successful'
                payload = json.dumps({'timestamp': datetime.datetime.now().strftime("%H:%M %d.%m.%y"), 'sender': 'server', 'response': 'info', 'content': info})
                self.connection.send(payload)
                if history != []:
                    payload = json.dumps({'timestamp': datetime.datetime.now().strftime("%H:%M %d.%m.%y"), 'sender': 'server', 'response': 'history', 'content': history})
                    self.connection.send(payload)

            else:
                raise Exception("Username taken.")
        else:
            raise Exception('Username unvalid. Try another username with A-Z, a-z, 0-9.')

    def logout(self):
        try: 
            if self in connectedClients:
                connectedClients.remove(self)           #Fjerner klient fra listen connectedClients
            if self.username in taken_usernames:
                taken_usernames.remove(self.username)   #Fjerner brukernavn fra listen taken_usernames
            self.connection.close()
            print 'User: %s has logged out' % self.username #Kan man aksessere self.username når har closed?
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
            payload = json.dumps({'timestamp': datetime.datetime.now().strftime("%H:%M %d.%m.%y"), 'sender': "Server", 'response': 'info' ,'content': names})
            self.connection.send(payload)
        except:
            raise Exception('Retrieving names failed.')

    def help(self):
        try:
            helpMessage = '\nAll commands:\nlogin <username>\nlogout\nmsg <message>\nnames\nhelp'
            payload = json.dumps({'timestamp': datetime.datetime.now().strftime("%H:%M %d.%m.%y"), 'sender': "Server", 'response': 'info' ,'content': helpMessage})
            self.connection.send(payload)
        except:
            raise Exception('Retrieving info failed.')




class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
