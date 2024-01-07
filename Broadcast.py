import time
import imagezmq
from Cameras.CameraStream import CameraStream
from Cameras.CameraModel import CameraModel
from Cameras.CameraType import CameraType
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True,
	help="Camera name")
ap.add_argument("-t", "--type", required=True,
	help="Camera type")
ap.add_argument("-ip", "--ip_addr", required=False,
	help="IP address")

if __name__ == "__main__":
    args = vars(ap.parse_args())

    name = args["name"]
    cam_type = CameraType[args["type"]]
    ip = args["ip_addr"]
    sender = imagezmq.ImageSender(connect_to='tcp://localhost:5555')

    model = CameraModel(name, type=cam_type, ip_addr=ip)
    cam = CameraStream(model).start()
    time.sleep(2.0)  # allow camera sensor to warm up

    while True:
        image = cam.read()
        sender.send_image(cam.model.name, image)
