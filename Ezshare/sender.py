import socket
import pickle
import file
import utils

class senderSocket:
    def __init__(self,sendBridge:utils.sendThreadBridge):
        self.sendBridge=sendBridge
        self.socket=socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
    def connect(self,ip_address):
        self.port=9999
        self.address=(ip_address,self.port)
        try:
            self.socket.connect(self.address)
        except:
            self.sendBridge.connection_failed=True

    def send_data(self,fileObj:file.File):
        data=pickle.dumps(fileObj)
        try:
            self.socket.sendall(data)
            self.socket.close()
            self.sendBridge.send_finished=True
        except:
            self.sendBridge.send_failed=True



