import cv2, threading
import depthai as dai
from .CameraType import CameraType

class CameraStream:
    """
    An object that reads frames from a camera.

    Attributes:
        model (CameraModel): A CameraModel instance.
        stream (cv2.VideoCapture): A VideoCapture instance.
        frame (numpy.ndarray): A frame from the camera.
        stopped (bool): A boolean indicating if the thread should be stopped.
    
    """

    def __init__(self, model):
        """
        Initializes a CameraStream instance.
        
        Parameters:
            model (CameraModel): A CameraModel instance.
        """

        self.model = model
        # initialize the video camera stream 
        # and read the first frame from the stream
        self.stream = self.get_stream()
		
        # initialize the variable used to indicate if the thread should
		# be stopped
        self.stopped = False


    def start(self):
		# start the thread to read frames from the video stream
        threading.Thread(target=self.update, args=()).start()
        return self
    
    
    def update(self):
		# keep looping infinitely until the thread is stopped
        while True:
			# if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
			# otherwise, read the next frame from the stream
            if (self.model.type == CameraType.OAK):
                q = self.stream.getOutputQueue(name="rgb", maxSize=4, blocking=False)
                preview = q.get()
                self.frame = preview.getCvFrame()
            else:
                _, self.frame = self.stream.read()


    def read(self):
		# return the frame most recently read
        return self.frame
    
    
    def stop(self):
		# indicate that the thread should be stopped
        self.stopped = True
        
    
    def get_stream(self):
        """Checks the type of camera and returns the appropriate stream."""
        if (self.model.type == CameraType.OAK):
            # Create pipeline
            pipeline = dai.Pipeline()

            # Define sources and outputs
            cam_rgb = pipeline.create(dai.node.ColorCamera)
            xout_rgb = pipeline.create(dai.node.XLinkOut)
            xout_rgb.setStreamName("rgb")

            # Properties
            cam_rgb.setPreviewSize(640, 480)
            cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
            cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)

            cam_rgb.preview.link(xout_rgb.input)

            return dai.Device(pipeline)

        else:
            cap = cv2.VideoCapture(self.model.src)

            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            return cap