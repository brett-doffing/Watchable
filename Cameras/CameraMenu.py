import os
from tkinter import *
import subprocess
from .CameraType import CameraType

class CameraMenu(Toplevel):
    def __init__(self, parent, broadcasts):
        Toplevel.__init__(self, parent)
        self.broadcasts = broadcasts
        self.title('Broadcast Camera')
        self.geometry('300x200')
        self.ip_addr = None
        self.strSelectedType = StringVar()
        self.strSelectedType.set(CameraType.USB.name)
        self.container = Frame(self)
        self.container.pack()
        self.dropDown = OptionMenu(self.container, self.strSelectedType, *[x.name for x in CameraType], command=self.selected)
        # self.dropDown.config(width=100)
        self.dropDown.pack(padx=10, pady=10, expand=1, fill=X)
        self.entry_ip = Entry(self.container, state=DISABLED)
        self.entry_ip.pack(ipady=3, padx=10, expand=1, fill=X)
        self.btnBroadcast = Button(self, text='Broadcast', command=self.broadcast)
        self.btnBroadcast.pack(side=BOTTOM, pady=10)


    def broadcast(self):
        cam_type = CameraType[self.strSelectedType.get()]
        cwd = os.getcwd()
        index = len(self.broadcasts) + 1
        process = subprocess.Popen(['python', f'{cwd}/broadcast.py', '-n', f'Cam {index}', '-t', cam_type.name]) # TODO: Assure Directory
        self.broadcasts.append(process)
        self.destroy()


    def selected(self, strType):
        cam_type = CameraType[strType]
        if cam_type is CameraType.IP or cam_type is CameraType.ESP32:
            self.entry_ip.configure(state=NORMAL)
        else:
            self.entry_ip.configure(state=DISABLED)
