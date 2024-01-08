import imagezmq
import threading

class ZMQHub():
    """
    An object that receives frames from a ZMQ broadcast.

    Attributes:
        image_hub (imagezmq.ImageHub): An ImageHub instance.
        models (dict): A dictionary of CameraModel instances.
        q (Queue): A queue of image frames.
        thread (threading.Thread): A thread that receives frames.
    """
    def __init__(self, q):
        """
        Initializes a ZMQHub instance.

        Parameters:
            q (Queue): A queue of image frames.
        """
        self.image_hub = imagezmq.ImageHub()
        self.q = q
        self.thread = threading.Thread(target=self.start)
        self.thread.daemon = True
        self.thread.start()

    def start(self):
        """Receives frames from the ZMQ broadcast and adds them to the queue."""
        while True:
            host_name, image = self.image_hub.recv_image()
            self.q.put({'frame': image, 'name': host_name})
            self.image_hub.send_reply(b'OK')
              
    def close(self):
        self.image_hub.close()         
