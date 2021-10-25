class File:
    def __init__(self,filename):
        self.filename=filename
        fil=open(filename,'rb')
        self.data=fil.read()
        fil.close()

    def save_self(self):
        fil=open(self.filename,'wb')
        fil.write(self.data)
        fil.close()
    