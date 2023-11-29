from tkinter import *
from tkCamera import tkCamera
from collections import OrderedDict
from ZMQHub import ZMQHub
import threading
from queue import Queue, Empty

class CamsView(Frame):
    def __init__(self, parent):
        """TODO: add docstring"""
        Frame.__init__(self, parent)

        self.parent = parent
        self.stream_widgets = []
        self.frame_buffer = {}
        self.q = Queue(maxsize=1)

        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)

        # columns = 3
        # for i in range(6):
        #     cam = tkCamPlaceholder(self.parent, name=f"Cam {i}")
        #     row = i // columns
        #     col = i % columns
        #     cam.grid(row=row, column=col)
        #     cam.update()

        self.hub = Hub(self.q)
        self.after(1, self.process_queue)

    def process_queue(self):
        # print("[App] process_frame")
        try:
            cam_dict = self.q.get_nowait()
            # self.q.task_done()
            self.process_frame(cam_dict)
                
        except Empty:
            pass
        # else:
        #     # print(f'Processing item {cam_dict["name"]}')
        #     self.process_frame(cam_dict)
        #     # q.task_done()
        self.after(1, self.process_queue)

    def add_camera_widget(self, cam_name):
        """TODO: add docstring"""
        widget = tkCamera(self.parent, cam_name)
        self.stream_widgets.append(widget)

    def update_feeds(self):
        """TODO: add docstring"""
        columns = 3
        for number, widget in enumerate(self.stream_widgets):
            if widget.name in self.frame_buffer:
                img = self.frame_buffer[widget.name]
                row = number // columns
                col = number % columns
                widget.grid(row=row, column=col)
                widget.update_feed(img)

    def process_frame(self, cam_dict):
        """TODO: add docstring"""
        name = cam_dict['name'] 
        frame = cam_dict['frame']
        # frame = draw_marker_detections(frame)
            
        self.frame_buffer[name] = frame

        contains = False
        for widget in self.stream_widgets:
            if widget.name == name:
                contains = True
        if not contains:
            self.add_camera_widget(name)

        self.update_feeds()

    def on_closing(self, event=None):
        """TODO: add docstring"""

        print("[App] stopping threads")
        self.hub.close()
        for widget in self.stream_widgets:
            widget.isRunning = False

        print("[App] exit")
        self.parent.destroy()

            
