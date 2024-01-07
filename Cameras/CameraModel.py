from .CameraType import CameraType

class CameraModel(object):
    def __init__(self, cam_name, type = CameraType.USB, ip_addr = None):
        # TODO: Assure ip_addr when necessary
        self.type = type
        self.ip_addr = ip_addr
        self.name = cam_name
        self.src = self.get_source()

    def __hash__(self):
        return hash(str(self))
    
    def get_source(self):
        if (self.type == CameraType.USB):
            return 0
        elif (self.type == CameraType.IP):
            return f'http://{self.ip_addr}'
        elif (self.type == CameraType.ESP32):
            return f'http://{self.ip_addr}:81/stream'
        else:
            return None