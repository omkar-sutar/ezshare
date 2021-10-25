#A file to keep all utility classes/funcs

class receiveThreadBridge:
    """A class to communicate between tk gui(main thread) and receive thread. \n Pass this object to the new thread func and 
    keep checking its status in main thread"""
    def __init__(self):
        self.receive_finished=False 
        self.receive_started=False

class sendThreadBridge:
    """A class to communicate between tk gui(main thread) and send thread. \n Pass this object to the new thread func and 
        keep checking its status in main thread"""

    def __init__(self):
        self.send_started=False
        self.send_finished=False
        self.connection_failed=False
        self.send_failed=False