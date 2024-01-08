from .CameraType import CameraType

class CameraModel(object):
    """
    A model for a camera.

    Attributes:
        type (CameraType): The type of camera.
        ip_addr (str): The IP address of the camera.
        name (str): The name of the camera.
        src (str): The source of the camera.
    """

    def __init__(self, cam_name, type = CameraType.USB, ip_addr = None):
        """
        Initializes a CameraModel instance.

        Parameters:
            cam_name (str): The name of the camera.
            type (CameraType): The type of camera.
            ip_addr (str): The IP address of the camera.
        """
        # TODO: Assure ip_addr and validity when necessary
        self.type = type
        self.ip_addr = ip_addr
        self.name = cam_name
        self.src = self.get_source()


    def __hash__(self):
        return hash(str(self))
    
    
    def get_source(self):
        """Checks the type of camera and returns the source."""
        if (self.type == CameraType.USB):
            return 0
        elif (self.type == CameraType.IP):
            return f'http://{self.ip_addr}'
        elif (self.type == CameraType.ESP32):
            return f'http://{self.ip_addr}:81/stream'
        else:
            return None