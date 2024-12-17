# MODULES
import socket
import threading
from time import sleep
import json

# CLASSES
class Connection:
    instances = []

    def __init__(self, conn:socket.socket, addr):
        self.__class__.instances.append(self)

        self.connection = conn
        self.address = addr
        self.connectionTimeout = 300.0
        self.emptyPacketCounter = 0

        # Automatically handle connection
        self.thread = threading.Thread(target=self.handle)
        self.thread.daemon = True
        self.thread.start()
    
    def verifyPacket(self, packet_data:str):
        """
        Returns True if packet structure is valid
        Returns False otherwise
        """
        
        if packet_data.strip() == '':
            self.emptyPacketCounter += 1
            return False
        
        try:
            # Check json structure
            json.loads(packet_data)
        except:
            return False
        
        # Valid Packet
        return True
    
    def sendRequest(self, header:list, body):
        # Jsonize request
        json_string = json.dumps({
            "header": header,
            "body": body
        })
        
        self.connection.send(json_string.encode('utf-8'))
        
    def executeRequest(self, request_type, request_content):
        if request_type == 'ping':
            # Send ping response
            h = [1, 'response']
            b = {'request_content':request_content, 'request_response':'pingok'}

        else:
            # Unknow request
            print('Unknow request :', request_type)
            return
        
        self.sendRequest(header=h, body=b)
    
    def treatPacket(self, packet_data):
        # Convert to JSON
        json_data = json.loads(packet_data)
        
        # Check finished-flag
        if json_data['header'][0]:
            finished = True
        
        while not finished:
            # Append remaining data to body > request-content
            nextData = self.connection.recv(1024).decode('utf-8')
            nextData_loaded = json.loads(nextData)
            json_data['body']['request_content'] += nextData_loaded['body']['request_content']
            
            # Check if finished
            if nextData['header'][0]:
                finished = True
        
        # Execute request
        req_type = json_data['header'][1]
        req_content = json_data['body']['request_content']
        self.executeRequest(req_type, req_content)
    
    def handle(self):
        self.connection.settimeout(self.connectionTimeout)
        while True and self.emptyPacketCounter < 10:
            try:
                # WAIT FOR PACKET
                data = self.connection.recv(1024).decode('utf-8')
                
                # VERIFY DATA
                if self.verifyPacket(data):    
                    # TREAT PACKET
                    self.treatPacket(data)
                else:
                    print(f'Invalid packet >> {data} <<')
                
            except ConnectionAbortedError:
                # Close connection
                break
            except TimeoutError:
                print('Timeout error, closing connection')
                break
        
        self.close()
        
    def close(self):
        self.connection.close()
        self.__class__.instances.remove(self)
        print('Connection closed on : ', self.address)

class Listener:
    def __init__(self, shost, sport):
        self.host = shost
        self.port = sport

        self.listening = False
        self.acceptTimeout = 0.5
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

    def start(self):
        self.listening = True
        self.socket.listen()
        self.socket.settimeout(self.acceptTimeout)
        print('Listening...')
        while self.listening:
            sleep(1.5)
            try:
                conn, addr = self.socket.accept()
                Connection(conn, addr)
            except TimeoutError:
                pass



if __name__ == '__main__':
    # START LISTENER
    listener = Listener("127.0.0.1", 8888)
    listener.start()