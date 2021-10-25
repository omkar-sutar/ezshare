import socket
import pickle
import file
import utils

class receiverSocket:
    def __init__(self,receiveBridge:utils.receiveThreadBridge):
        self.receiveBridge=receiveBridge
        self.socket=socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
        self.host_name=socket.gethostname()
        self.host_ip=socket.gethostbyname(self.host_name)
        #This port will be used for transmission on both sender and receiver
        self.port=9999
        self.address=(self.host_ip,self.port)
    
    def get_address(self):
        return self.address

    def bind(self):
        self.socket.bind(self.address)
        self.socket.listen(1)

    def get_data(self)->file.File:
        self.senderSocket,self.senderAddr=self.socket.accept()
        self.receiveBridge.receive_started=True
        chunks=[]
        while True:
            chunk=self.senderSocket.recv(1024)
            if not chunk:
                break
            chunks.append(chunk)
        data=b''.join(chunks)
        #data is bytes object
        data=pickle.loads(data)
        self.receiveBridge.receive_finished=True
        #data is File object (file.File)
        return data

    def close_socket(self):
        self.socket.close()

