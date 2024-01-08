import os
from tkinter import *
import subprocess
from .CameraType import CameraType

class CameraMenu(Toplevel):
    """
    A tkinter Toplevel that allows the user to select a camera type and broadcast it from localhost.
    
    Attributes:
        parent (tkinter.Tk): The parent tkinter window.
        broadcasts (list): A list of processes.
        strSelectedType (tkinter.StringVar): The selected camera type.
        container (tkinter.Frame): The container frame.
        dropDown (tkinter.OptionMenu): The dropdown menu.
        ip_text (tkinter.StringVar): The IP address entry text.
        entry_ip (tkinter.Entry): The IP address entry.
        btnBroadcast (tkinter.Button): The broadcast button.
    """
    
    def __init__(self, parent, broadcasts):
        """
        Initializes a CameraMenu instance.
        
        Parameters:
            parent (tkinter.Tk): The parent tkinter window.
            broadcasts (list): A list of processes.
        """
        Toplevel.__init__(self, parent)
        self.broadcasts = broadcasts
        self.title('Broadcast Camera')
        self.geometry('300x200')
        self.strSelectedType = StringVar()
        self.strSelectedType.set(CameraType.USB.name)
        self.container = Frame(self)
        self.container.pack()
        self.dropDown = OptionMenu(self.container, self.strSelectedType, *[x.name for x in CameraType], command=self.selected)
        self.dropDown.pack(padx=10, pady=10, expand=1, fill=X)
        self.ip_text = StringVar()
        self.entry_ip = Entry(self.container, state=DISABLED, textvariable=self.ip_text)
        self.entry_ip.pack(ipady=3, padx=10, expand=1, fill=X)
        self.btnBroadcast = Button(self, text='Broadcast', command=self.broadcast)
        self.btnBroadcast.pack(side=BOTTOM, pady=10)


    def broadcast(self):
        """Broadcasts the selected camera type from localhost by running Broadcast.py script with the selected arguments."""
        cam_type = CameraType[self.strSelectedType.get()]
        cwd = os.getcwd()
        index = len(self.broadcasts) + 1

        # TODO: Assure Directory is correct
        process = subprocess.Popen(['python', f'{cwd}/Broadcast.py', '-n', f'Cam {index}', '-t', cam_type.name, '-ip', self.ip_text.get()]) 
        self.broadcasts.append(process)
        self.destroy()


    def selected(self, strType):
        """
        Callback function for the dropdown menu. Enables the IP address entry if the selected type is IP or ESP32.
        """
        cam_type = CameraType[strType]
        if cam_type is CameraType.IP or cam_type is CameraType.ESP32:
            self.entry_ip.configure(state=NORMAL)
        else:
            self.entry_ip.configure(state=DISABLED)
