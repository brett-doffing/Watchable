from tkinter import *
from PIL import Image
from PIL import ImageTk
from Hub import Hub
import cv2

class tkCamera(Frame):
    def __init__(self, parent, name=""):
        """TODO: add docstring"""
        Frame.__init__(self, parent, highlightbackground="black", highlightthickness=1)

        self.name = name
        self.width  = 320
        self.height = 240
        # self.other_sources = sources

        # self.cam = Camera(name)
        # self.config(highlightcolor="gray", highlightthickness=1)
        
        self.label = Label(self, text=name)
        self.label.pack()

        self.canvas = Button(self, width=self.width, height=self.height)
        self.canvas.pack()

        # Button that lets the user record video
        self.btn_snapshot = Button(self, text="Add", command=self.start)
        self.btn_snapshot.pack(anchor='center', side='left')

        self.btn_snapshot = Button(self, text="Stop", command=self.stop)
        self.btn_snapshot.pack(anchor='center', side='left')

        # Button that lets the user take a snapshot
        self.btn_snapshot = Button(self, text="Snapshot", command=self.snapshot)
        self.btn_snapshot.pack(anchor='center', side='left')

        # Button that lets the user select source
        # self.btn_snapshot = Button(self, text="Source", command=self.select_source)
        # self.btn_snapshot.pack(anchor='center', side='left')

        # After it is called once, the update method will be automatically called every delay milliseconds
        # calculate delay using `FPS`
        # self.delay = int(1000/self.vid.fps)

        print('[tkCamera] source:', self.name)
        # print('[tkCamera] fps:', self.vid.fps, 'delay:', self.delay)

        self.image = None
        self.dialog = None
    
    def start(self):
        """TODO: add docstring"""

        #if not self.running:
        #    self.running = True
        #    self.update_frame()
        # self.vid.start_recording()

    def stop(self):
        """TODO: add docstring"""

        #if self.running:
        #   self.running = False
        # self.vid.stop_recording()

    def snapshot(self):
        """TODO: add docstring"""

        # Get a frame from the video source
        #ret, frame = self.vid.get_frame()
        #if ret:
        #    cv2.imwrite(time.strftime("frame-%d-%m-%Y-%H-%M-%S.jpg"), cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))

        # Save current frame in widget - not get new one from camera - so it can save correct image when it stoped
        #if self.image:
        #    self.image.save(time.strftime("frame-%d-%m-%Y-%H-%M-%S.jpg"))

        # self.vid.snapshot()

    def update_feed(self, img):
        """TODO: add docstring"""

        # widgets in tkinter already have method `update()` so I have to use different name -

        # Get a frame from the video source
        # frame = self.cam.read()

        if img is not None:
            self.image = img
            image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.image = Image.fromarray(image)
            self.photo = ImageTk.PhotoImage(image=self.image)
            self.canvas.config(image=self.photo)
            self.canvas.image = self.photo
            # self.canvas.create_image(0, 0, image=self.photo, anchor='nw')
            
        self.canvas.update()

        # if self.running:
        #     self.after(1, self.update_frame)

    # def select_source(self):
    #     """TODO: add docstring"""

    #     # open only one dialog
    #     if self.dialog:
    #         print('[tkCamera] dialog already open')
    #     else:
    #         self.dialog = tkSourceSelect(self, self.other_sources)

    #         self.label['text'] = self.dialog.name
    #         self.source = self.dialog.source

    #         self.vid = MyVideoCapture(self.source, self.width, self.height)