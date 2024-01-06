# run this program on each camera host to send a labelled image stream
import time
import imagezmq
from CameraStream import CameraStream
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True,
	help="Camera name")

args = vars(ap.parse_args())

name = args["name"]
sender = imagezmq.ImageSender(connect_to='tcp://localhost:5555')

cam = CameraStream(name).start()
time.sleep(2.0)  # allow camera sensor to warm up

while True:  # send images as stream until Ctrl-C
    image = cam.read()
    sender.send_image(cam.model.name, image)