import socket
import time
import json

"""Module for streamer implementations
    
Streamers are meant to stream data to an external client;

Todo:
    * add an interface class for the concrete streamer classes

"""

class SimpleStreamer:
    """Simple implementation of a streamer.

    It uses a TCP connection to stream data.

    """

    def __init__(self, host, port):
        """
            Args:
                host (str): streamer's destination host address
                port (str): streamer's destination host port

            Attributes:
                connection (obj): connection to the client
                _host (str): client address
                _port (str): client port

        """

        self.connection = None
        self._host = host
        self._port = port    
        
    def create_connection(self):
        """ Establishes a connection.

        This method create a connection to the client and naively handle occasional connection problems

        """

        tryouts = 0
        
        while self.connection is None:
            try:
                print(f'Create connection: try n° {tryouts + 1}')
                self.connection = socket.create_connection((self._host, self._port))
                print("Connection established")
            except Exception as e:
                tryouts += 1
                print(repr(e))
                print("Sleeping for 10 sec")
                time.sleep(10)

        return self  

    def send(self, payload):
        """ Streams data to the client.

        In addition to send the data, handle occasional connection problem using create_connection

        """

        while True:
            try:
                self.connection.sendall(
                    self._format_payload(payload)
                    )
                return
            except OSError:
                self.connection = None
                self.create_connection()



    def _format_payload(self, payload):
        """ Format the data to be send """
        
        formatted_payload = {"data": payload.dict()}
        return (json.dumps(formatted_payload, default=str) + '\n').encode()
        
                


    

        