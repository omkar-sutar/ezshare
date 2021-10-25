import tkinter as tk
from tkinter.filedialog import askopenfilename,asksaveasfilename
from tkinter.messagebox import showerror, showerror, showinfo
from tkinter import font
import threading

import receiver
import sender
import file
import utils

class App:
    def __init__(self):
        self.root=tk.Tk()
        self.root.geometry("360x360")
        self.root.title(string="EzShare")
        self.root.resizable(width=False,height=False)
        self.screen0()
    def screen0(self):
        self.frame=tk.Frame(master=self.root,bg='white')
        sendBtn=tk.Button(master=self.frame,text="Send",background="#2777C2",foreground="#FFFFFF",width=10,command=self.actionSend)
        sendBtn.pack(pady=(130,0))
        recvBtn=tk.Button(master=self.frame,text="Receive",background="#2777C2",foreground="#FFFFFF",width=10,command=self.actionRecv)
        recvBtn.pack(pady=(20,110))
        self.frame.pack(expand=True,fill=tk.BOTH)

    def actionRecv(self):
        self.receiveBridge=utils.receiveThreadBridge()
        self.receiveSocket=receiver.receiverSocket(self.receiveBridge)
        address=self.receiveSocket.get_address()
        self.receiveSocket.bind()
        self.screenReceive0(address)

    def screenReceive0(self,address):
        #"Waiting for Sender..."" screen
        self.frame.destroy()
        self.frame=tk.Frame(master=self.root,bg='white')
        goodFont=font.Font(size=13)
        ip_addr=tk.Label(master=self.frame,text=f'IPv4: {address[0]}',background="#FFFFFF",font=goodFont)
        port=tk.Label(master=self.frame,text=f'Port: {address[1]}',background="#FFFFFF",font=goodFont)
        label=tk.Label(master=self.frame,text="Waiting for Sender...",background="#FFFFFF",font=goodFont)
        ip_addr.pack(pady=(110,0))
        port.pack(pady=(20,0))
        label.pack(pady=(20,0))
        self.frame.pack(expand=True,fill=tk.BOTH)

        #Start new thread for receive
        threading.Thread(target=self.get_file).start()
        self.frame.after(200,func=self.update_screenReceive0)


    def update_screenReceive0(self):
        if self.receiveBridge.receive_started==True:
            self.screenReceive1()
            
        else:
            self.frame.after(200,func=self.update_screenReceive0)

    

    def get_file(self):
        self.fileObj=self.receiveSocket.get_data()
    def screenReceive1(self):
        #"Receiving file..." screen
        self.frame.destroy()
        self.frame=tk.Frame(master=self.root,bg='white')
        goodFont=font.Font(size=13)
        receiveLabel=tk.Label(master=self.frame,text="Receiving File...",font=goodFont,background="#FFFFFF")
        receiveLabel.pack(pady=(110,0))
        self.frame.pack(expand=True,fill=tk.BOTH)
        self.frame.after(200,func=self.update_screenReceive1)
    
    def update_screenReceive1(self):
        if self.receiveBridge.receive_finished==True:
            self.screenReceive2()
        else:
            self.frame.after(200,func=self.update_screenReceive1)
    
    def screenReceive2(self):
        #"File received!" and Save File screen
        self.frame.destroy()
        self.frame=tk.Frame(master=self.root,bg='white')
        goodFont=font.Font(size=13)
        receivedLabel=tk.Label(master=self.frame,text="File Received!",font=goodFont,background="#FFFFFF")
        receivedLabel.pack(pady=(110,0))

        saveBtn=tk.Button(master=self.frame,text="Save As",foreground="#FFFFFF",
                            background="#2777C2",activeforeground="#FFFFFF",
                            activebackground="#0555A0",width=9,
                            command=self.save_file)

        saveBtn.place(x=260,y=300)
        self.frame.bind('<Return>',func=lambda event: self.save_file)

        cancelBtn=tk.Button(master=self.frame,text="Cancel",foreground="#FFFFFF",
                            background="#919191",activeforeground="#FFFFFF",
                            activebackground="#919191",width=9,
                            command=lambda : (self.frame.destroy(),self.screen0()))
        cancelBtn.place(x=180,y=300)

        self.frame.pack(expand=True,fill=tk.BOTH)
    
    def save_file(self):
        filename_noExt=self.fileObj.filename[self.fileObj.filename.rfind('/')+1:self.fileObj.filename.rfind('.')]
        fileExtension=self.fileObj.filename[self.fileObj.filename.rfind('.'):]
        filename=filename_noExt+fileExtension
        filename=asksaveasfilename(initialfile=filename,defaultextension=fileExtension)
        if filename==None or filename=='':
            return
        self.fileObj.filename=filename
        self.fileObj.save_self()



    def actionSend(self):
        self.sendBridge=utils.sendThreadBridge()
        self.sendSocket=sender.senderSocket(self.sendBridge)
        
        filename=self.choose_file()
        if filename=='':
            return
        self.screenSend0()
        
    def choose_file(self):
        """Gets the filename through Windows file explorer"""
        filename=askopenfilename()
        if filename=='':
            return ''
        self.fileObj=file.File(filename)
        
    
    def screenSend0(self):
        #"IP address and Choose file" screen
        #TODO remove try except
        try:
            self.frame.destroy()
        except:
            pass
        self.frame=tk.Frame(master=self.root,background="#FFFFFF")
        goodFont=font.Font(size=13)
        ipAddr_label=tk.Label(master=self.frame,text="IPv4: ",font=goodFont,background="#FFFFFF")
        ipAddr_label.place(x=90,y=90)
        ipAddr_entry=tk.Entry(master=self.frame,background="#FFFFFF",bd=1)
        ipAddr_entry.place(x=150,y=93)
        ipAddr_entry.focus()

        nextBtn=tk.Button(master=self.frame,text="Next",foreground="#FFFFFF",background="#2777C2",
                            activeforeground="#FFFFFF",activebackground="#0555A0",width=9,
                            command=lambda: self.screenSend1(ipAddr_entry.get()))
        #TODO add a Back button
        ipAddr_entry.bind('<Return>',func=lambda event: self.screenSend1(ipAddr_entry.get()))
        nextBtn.place(x=260,y=300)
        self.frame.pack(expand=True,fill=tk.BOTH)

    def screenSend1(self,ipAddr:str):
        #Check if ipAddr is valid
        if ipAddr.count('.')!=3:
            showerror(title="EzShare",message="Invalid IP address")
            return

        self.frame.destroy()
        self.frame=tk.Frame(master=self.root,background="#FFFFFF")
        goodFont=font.Font(size=13)
        sendingLabel=tk.Label(master=self.frame,text="Sending file...",font=goodFont,background="#FFFFFF")
        sendingLabel.pack(pady=(110,0))



        self.frame.pack(expand=True,fill=tk.BOTH)

        threading.Thread(target=self.send_file,args=(ipAddr,)).start()
        self.frame.after(200,self.update_screenSend1)

    def send_file(self,ipAddr):
        self.sendSocket.connect(ipAddr)
        self.sendSocket.send_data(self.fileObj)

    def update_screenSend1(self):
        if self.sendBridge.send_finished==True:
            showinfo(title="EzShare",message="File transfer Successfull!")
            self.frame.destroy()
            self.screen0()
            return
        elif self.sendBridge.connection_failed==True:
            showerror(title="EzShare",message="File transfer Failed: Receiver unreachable")
            self.screenSend0()
            return
        elif self.sendBridge.send_failed==True:
            showerror(title="EzShare",message="File transfer Failed!")
            self.frame.destroy()
            self.screenSend0()
            return

        self.frame.after(200,self.update_screenSend1)




    
if __name__ == '__main__':
    app=App()
    app.root.mainloop()


