from tkinter import *
from TKCamera import TKCamera
from collections import OrderedDict
from ZMQHub import ZMQHub
from queue import Queue, Empty
import cv2
import numpy as np
from Calibration import Calibrate

class CamsView(Frame):
    """
    A class representing A tkinter Frame that displays multiple camera feeds.
 
    Attributes:
        parent (tkinter.Tk): The parent tkinter window.
        stream_widgets (list): A list of TKCamera widgets.
        frame_buffer (dict): A dictionary of frames.
        q (Queue): A queue of frames.
        hub (ZMQHub): A ZMQHub instance.
    """

    def __init__(self, parent):
        """
        Initializes a CamsView instance.

        Parameters:
            parent (tkinter.Tk): The parent tkinter window.
        """
        Frame.__init__(self, parent)

        self.parent = parent
        self.stream_widgets = []
        self.frame_buffer = {}
        self.q = Queue(maxsize=1)

        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.hub = ZMQHub(self.q)
        self.after(1, self.process_queue)


    def process_queue(self):
        """Grabs the latest frame from the queue and processes it."""
        try:
            cam_dict = self.q.get_nowait()
            self.process_frame(cam_dict)
        except Empty:
            pass

        self.after(1, self.process_queue)


    def add_camera_widget(self, cam_name):
        """
        Adds a new camera widget to the grid
        Parameters:
            cam_name (str): The name of the camera.
        """
        widget = TKCamera(self.parent, cam_name)
        self.stream_widgets.append(widget)


    def process_frame(self, cam_dict):
        """
        Processes a frame from the queue by adding it to the frame buffer and updating the feeds.
        Parameters:
            cam_dict (dict): A dictionary containing the name and image frame of the camera.
        """
        name = cam_dict['name'] 
        frame = cam_dict['frame']
            
        self.frame_buffer[name] = frame

        contains = False
        for widget in self.stream_widgets:
            if widget.name == name:
                contains = True
        if not contains:
            self.add_camera_widget(name)

        self.update_feeds()


    def update_feeds(self):
        """Updates the feeds of all the camera widgets."""
        columns = 3
        for number, widget in enumerate(self.stream_widgets):
            if widget.name in self.frame_buffer:
                img = self.frame_buffer[widget.name]
                row = number // columns
                col = number % columns
                widget.grid(row=row, column=col)
                widget.update_feed(img)


    def on_closing(self):
        """Called when the window is closed."""
        print("[App] stopping threads")
        self.hub.close()
        for widget in self.stream_widgets:
            widget.isRunning = False

        print("[App] exit")
        self.parent.destroy()


    def calibrate(self):
        """
        Called when the calibrate menu bar option is pressed.
        Saves the images of the camera widgets to the Calibration/images folder.
        Runs the calibration process.
        """
        for widget in self.stream_widgets:
            cv2.imwrite(f"Calibration/images/{widget.name}.jpg", np.array(widget.image))

        Calibrate.run()