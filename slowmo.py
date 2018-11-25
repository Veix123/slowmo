#!/usr/bin/python

from gpiozero import PWMLED, Button
import os
import io
import picamera
from time import sleep

cam = picamera.PiCamera()
cam.resolution = (640, 480)
cam.framerate = 90

print("Starting stream")
stream = picamera.PiCameraCircularIO(cam, seconds=2)

print("Starting camera")
cam.start_recording(stream, format='h264')

trigger = Button(2)
laser = PWMLED(3)
laser.value = 0.8

cam.wait_recording(1)

try:
  while 1:
    if trigger.is_pressed==True:
      print("Recording...")
      cam.wait_recording(1)
      stream.copy_to('sample90fps.h264', seconds=2)

      os.system('MP4Box -fps 10 -add sample90fps.h264 sample.mp4')
      os.system('omxplayer sample.mp4')
      os.system('rm sample.mp4')
    sleep(0.05)
finally:
  cam.stop_recording()
