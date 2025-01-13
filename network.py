from PyQt6.QtCore import pyqtSignal, QObject
import socket
import threading
from time import sleep, time
import json
import conversion

# DEFAULT PACKET VALUES (tuple : header, body)
PING_PACKET = ([1, 'ping'], {'request_content':'azerty', 'request_response':'azerty'})


# Connection > Parent Class
class Connection(QObject):
    instances = [] # Contains every connections
    
    # Signal emitted only from client
    main_signal = pyqtSignal(QObject)
    
    ping_updated = pyqtSignal(float) # Create Signal
    emptyPackets_updated = pyqtSignal(int) # Create Signal
    packetsCounter_updated = pyqtSignal(int) # Create signal    
    
    def __init__(self, conn:socket.socket, addr):
        # Update instances list
        Connection.instances.append(self)
        
        # Init PyQt6 Object (used for signals)
        super().__init__()
        
        
        # Attributes
        self.connection = conn
        self.address = addr
        self.connectionTimeout = 300.0
        self._packetsCounter = 0
        self._emptyPacketCounter = 0
        self.maxEmptyPacket = 10
        self._ping = 0
        self.lastPacketSendTime = 0.0
        self.lastPacketRecvTime = 0.0

    @property
    def packetsCounter(self):
        return self._packetsCounter
    
    @packetsCounter.setter
    def packetsCounter(self, value):
        if self._packetsCounter != value:
            self._packetsCounter = value
            # Emit signal
            self.packetsCounter_updated.emit(self._packetsCounter)

    @property
    def emptyPacketCounter(self):
        return self._emptyPacketCounter
    
    @emptyPacketCounter.setter
    def emptyPacketCounter(self, value):
        if self._emptyPacketCounter != value:
            self._emptyPacketCounter = value
            self.emptyPackets_updated.emit(self.emptyPacketCounter)

            # Check limit
            if self._emptyPacketCounter >= self.maxEmptyPacket:
                print(f'Empty packets {self._emptyPacketCounter} >> closing connection')
                self.close()

    @property
    def ping(self):
        return self._ping
    
    @ping.setter
    def ping(self, value):
        if self._ping != value:
            self._ping = value
            # Emit Signal when ping value changes
            self.ping_updated.emit(self._ping)

    def verifyPacket(self, packet_data:str):
        """
        Returns True if packet structure is valid & complete
        Returns False otherwise
        """
        
        print(f"""
____________________| Veryfing Packet |____________________
    Data ({type(packet_data)}): {packet_data}
""")
        
        if packet_data.strip() == '':
            return False
        
        json.loads(packet_data)
        try:
            # Check json structure
            json.loads(packet_data)
        except:
            print('loading json, error')
            return False
        
        # Valid Packet
        return True

    def sendPacket(self, header:list, body:dict):
        packet_size = 1024
        
        # Jsonize request
        json_string = json.dumps({
            "header": header,
            "body": body
        })
        
        # Update time (for ping calculation)
        self.lastPacketSendTime = time()
        
        # Encode packet
        packet_data = json_string.encode('utf-8')
        
        # Ensure packet size
        if len(packet_data) < packet_size:
            # Pad with null bytes
            padding_size = packet_size - len(packet_data)
            packet_data += b'\0' * padding_size
        
        # Send packet
        sent_size = self.connection.send(packet_data)
        
        # Update sent packet counter
        self.packetsCounter += 1
        
        print(f"""
____________________| Packet Sent |____________________  
    - HEADER ({type(header)}) : {header}
    - BODY ({type(body)}) :\t {body}
    - BYTES : {sent_size}
""")

    def listenForPackets(self):
        # Set listening timeout
        self.connection.settimeout(self.connectionTimeout)
        
        # Listening loop
        while True and self.emptyPacketCounter < self.maxEmptyPacket:
            try:
                # Wait for a packet
                recvd = self.connection.recv(1024).rstrip(b'\0')
                data = recvd.decode('utf-8')
                print(f"""
____________________| Received Packet |____________________
    Packet ({type(recvd)}): {recvd}
    Decoded ({type(data)}): {data}
""")
                self.packetsCounter += 1
                
                # Update ping
                self.lastPacketRecvTime = time()
                
                self.ping = (self.lastPacketRecvTime - self.lastPacketSendTime)
                
                # Valid packet strucure > Packet executed
                if self.verifyPacket(data):
                    
                    # Get full packet data
                    json_data = json.loads(data)
                    while json_data['header'][0] == 0:
                        print('Data incomplete > fetching next packet')
                        
                        # Fetch next packet
                        nextData = self.connection.recv(1024).rstrip(b'\0').decode('utf-8')
                        nextData_loaded = json.loads(nextData)

                        # Append new data
                        json_data['body']['request_content'] += nextData_loaded['body']['request_content']
                        
                        # Update header flag
                        json_data['header'][0] = nextData_loaded['header'][0]
                        
                    # Handle Packet
                    self.handleData(json_data)
                
                # Invalid packet structure > Packet lost
                else:
                    print(f'Invalid packet >> {data} <<')
                    self.emptyPacketCounter += 1
                
            except ConnectionAbortedError:
                print('Connection aborted')
                # Close connection
                break
            except TimeoutError:
                print('Timeout error, closing connection')
                break
        
        # Endloop > Disconnect
        self.close()

    def close(self):
        # Disconnect client from the server
        self.connection.close()
        
        # Remove client instance from the instances
        Connection.instances.remove(self)
        print('Connection closed on : ', self.address)

    def handleData(self, data):
        # Decompose data
        HEADER = data['header']
        BODY = data['body']
        
        # Extract header data
        data_flag = HEADER[0]
        request_type = HEADER[1]
        
        # Extract body data
        request_content = BODY['request_content']
        request_response = BODY['request_response']
        
        request_body_keys = list(BODY.keys())
        
        max = len(request_content)-1
        if len(request_content) > 100:
            max = 100
        print(f"""
____________________| Handling Data |____________________  
    - Data Flag : {data_flag}
    - Request Type : {request_type}
    - Request Content ({len(str(request_content))}) : {request_content[0:max]}
    - Request Response ({len(str(request_response))}) : {request_response}
    - Request Body keys : {request_body_keys}
""")
        
        
        # Default response packet
        R_HEADER = [1, 'none']
        R_BODY = {
            'request_content':request_content,
            'request_response':'received'
        }
        
        # Handle kind of request
        if request_type == 'ping':
            # Make header
            R_BODY['request_response'] = 'pingok'

        elif request_type == 'none':
            # No response
            return

        elif request_type == 'bytes_received':
            # Emit file-sent signal
            print('file received by host')
            
            # No response
            return

        elif request_type == 'file_transfer':
            # TMP
            decoded = conversion.unmakeSerializable(request_content)
            fname = BODY['filename']
            with open(fname, 'wb') as f:
                f.write(decoded)
            # TMP

            # Emit file-bytes-received signal
            print('file received with success')
        
            # Packet response > file-received
            R_HEADER[1] = 'bytes_received'
            R_BODY['request_response'] = ''
            R_BODY['request_content'] = 'file_received'

        else:
            # Unknow request
            print('Unknow request :', request_type)
            return
        
        # Send reponse packet to client
        self.sendPacket(header=R_HEADER, body=R_BODY)

    def refreshConnection(self):
        # Send ping packet
        self.sendPacket(PING_PACKET[0], PING_PACKET[1])

    def sendFile(self, file_bytes, filename):
        # Make bytes serializable
        file_bytes = conversion.makeSerializable(file_bytes)
        
        # Split bytes into packets of 512 bytes
        splitted = conversion.makeChunks(512, file_bytes)
        
        # Send each chunk at a time
        size_sent = 0
        for i in range(len(splitted)):
            chunk = splitted[i]

            # Body
            b = {
                'request_content':chunk,
                'request_response':''
            }
            
            # Add filename to first packet's body
            if i == 0:
                b['filename'] = filename
        
            data_flag = 0
            # Check if last packet
            if i == len(splitted) - 1:
                # Last chunk
                data_flag = 1
            # Header
            h = [data_flag, 'file_transfer']
            
            # Send
            self.sendPacket(h, b)
            
            # Update sent size
            size_sent += len(chunk)
        
        print('Total chunks size : ', size_sent)

# Server > Wait for packets from client and respond accordingly
class Server(Connection):
    instances = []
    
    def __init__(self, hostname:str, port:int):
        Server.instances.append(self)

        self.address = (hostname, port)
        self.listening = False
        self.acceptTimeout = 0.5
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.socket.bind(self.address)
        
        super().__init__(self.socket, self.address)
        
        # Start listener by default
        self.startListener()

    def startListener(self):
        self.listening = True
        self.socket.settimeout(self.acceptTimeout)
        self.socket.listen()
        
        # Thread listener
        self.thread = threading.Thread(target=self.listenForClient)
        self.thread.daemon = True
        self.thread.start()
        
    def listenForClient(self):
        print('Listening...')
        while self.listening:

            try:
                # Instanciate Client object
                conn, addr = self.socket.accept()
                c = ClientFromServer(conn, addr)
                
                # Emit signal for newly created client
                self.main_signal.emit(c)

            except TimeoutError:
                sleep(1.5)

    def refreshConnection(self):
        # Refresh the connection for the client-connection (instead of the server-connection)
        if len(ClientFromServer.instances) > 0:    
            ClientFromServer.instances[-1].refreshConnection()
        else:
            print('No connected clients')


# Client > Server Side
class ClientFromServer(Connection):
    instances = []
    
    def __init__(self, conn, addr):
        ClientFromServer.instances.append(self)
        
        super().__init__(conn, addr)
        
        # Automatically handle connection
        self.thread = threading.Thread(target=self.listenForPackets)
        self.thread.daemon = True
        self.thread.start()


# Client > Client Side
class Client(Connection):
    instances = []
    
    def __init__(self, host, port):
        Client.instances.append(self)
        
        # Connect to server
        self.connectAttempts = 1
        self.address = (host, port)
        
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        if not self.connectToServer(sock):
            # Remove client
            self.close()
            return
        
        super().__init__(sock, self.address)
        
        # Emit main signal
        self.main_signal.emit(self)
        
        # Automatically handle connection
        self.thread = threading.Thread(target=self.listenForPackets)
        self.thread.daemon = True
        self.thread.start()

    def close(self):
        # Remove client instance from the instances
        Client.instances.remove(self)
        
        print('Connection closed on : ', self.address)

    def connectToServer(self, sock):
        for _ in range(self.connectAttempts):
            
            # Try connecting
            try:
                sock.connect(self.address)
                return True
            
            except ConnectionRefusedError:
                sleep(1.0)
                
            except OSError:
                print('OSError : connection maybe already established')
        
        print('Could not connect to server :', self.address)
        return False