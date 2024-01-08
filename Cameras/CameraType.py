from enum import Enum

class CameraType(Enum):
    """An enumeration of camera types."""
    USB = 0
    OAK = 1
    IP = 2
    ESP32 = 3