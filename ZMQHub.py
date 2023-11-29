import imagezmq
from Camera_Model import Camera_Model
import threading
import multiprocessing
from queue import Queue
from collections import OrderedDict

class ZMQHub():
    def __init__(self, q):
        self.image_hub = imagezmq.ImageHub()
        self.models = {}
        self.q = q
        self.thread = threading.Thread(target=self.start)
        self.thread.daemon = True
        self.thread.start()

    def start(self):
        while True:
            host_name, image = self.image_hub.recv_image()

            if self.models.get(host_name, None) is None:
                self.models[host_name] = Camera_Model(host_name)

            self.q.put({'frame': image, 'name': host_name})
            self.image_hub.send_reply(b'OK')
              
    def close(self):
        self.image_hub.close()         
