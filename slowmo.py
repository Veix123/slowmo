#!/usr/bin/python

from gpiozero import PWMLED, Button
import os
import io
import picamera
from time import sleep

cam = picamera.PiCamera()
cam.resolution = (640, 480)
cam.framerate = 90
cam.vflip = True
cam.hflip = True

print("Starting stream")
stream = picamera.PiCameraCircularIO(cam, seconds=2)

#Start preview in a window
#cam.start_preview(fullscreen=False, window=(100,100,640,480))
cam.start_preview(fullscreen=True)

print("Starting camera")
cam.start_recording(stream, format='h264')

trigger = Button(2)
laser = PWMLED(3)
laser.value = 0.8

cam.wait_recording(1)

try:
  while 1:
    if trigger.is_pressed==False:
      print("Recording...")
      cam.wait_recording(1)
      stream.copy_to('sample90fps.h264', seconds=1.1)

      os.system('MP4Box -fps 10 -add sample90fps.h264 sample.mp4')
      cam.stop_preview()
      os.system('omxplayer sample.mp4')
      os.system('rm sample.mp4')
      #cam.start_preview(fullscreen=False, window=(100,100,640,480))
      cam.start_preview(fullscreen=True)
    sleep(0.05)
except KeyboardInterrupt:
  print("Got Interrupt, closing...")
  pass
finally:
  cam.stop_preview()
  cam.close()
  cam = 0

