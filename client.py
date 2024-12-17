import socket
import json
from time import sleep

h = "127.0.0.1"  # SERVER HOSTNAME
p = 8888         # SERVER PORT

class Connection:
    def __init__(self, host:str, port:int):
        self.host, self.port = host, port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        self.timeoutErrorCounter = 0
        # Establish connection
        self.connect()
        
    def connect(self):
        try:    
            self.connection.connect((self.host, self.port))
            self.timeoutErrorCounter = 0
        except TimeoutError:
            sleep(1.0)
            self.timeoutErrorCounter += 1

    def makeRequest(self, header, body):
        """
        Makes request from header/body values
        Returns the response from the server
        """
        # Make request
        json_string = json.dumps({
            "header": header,
            "body": body
        })

        # Send request
        self.connection.send(json_string.encode('utf-8'))

        # Receive response
        res = self.receivePacket()
        return res
    
    def receivePacket(self):
        pass
    
        # Receive response
        response = self.connection.recv(1024).decode('utf-8')
        return json.loads(response)
    
conn = Connection(h, p)

while True:
    req_type = input('Request type : ')
    req = input('Request : ')
    
    h=[1, req_type]
    b={
        'request_content':req,
        'request_response':''
    }
    # Send
    resp = conn.makeRequest(header=h, body=b)
    print('Response : ', resp)