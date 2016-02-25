# -*- coding: utf-8 -*-

"""
This is the message receiver class. The class inherits Thread, something that
is necessary to make the MessageReceiver start a new thread, and it allows
the chat client to both send and receive messages at the same time
"""


from threading import Thread

class MessageReceiver(Thread):

    def __init__(self, client, connection):

        Thread.__init__(self)
        self.daemon = True
        self.client = client
        self.connection = connection
        self.activated = True

    def run(self):
        # Loop while the connection is alive
        while self.activated:
            # Look for message
            try:
                msg = self.connection.recv(1024)

            except Exception as e:
                print(e.message)
                print('An error occured with connection to the server, please try to re-run')
                break

            # If there is no message, break out of the loop.
            if msg is None:
                break

            # If there is a message, then pass it on
            else:
                self.client.receive_message(msg)
        pass