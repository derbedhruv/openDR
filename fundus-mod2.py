import time
import cv2
import numpy as np
import pigpio
import picamera
import io
from picamera.array import PiRGBArray

led_top=2
led_bottom=3
capture_switch=4
i=1

# pi is initialized as the pigpio object
pi=pigpio.pi()

#set I/O modes for GPIOs
pi.set_mode(led_top,pigpio.OUTPUT)
pi.set_mode(led_bottom,pigpio.OUTPUT)
pi.set_mode(capture_switch,pigpio.INPUT)

#set a pull-up resistor on the switch pin
pi.set_pull_up_down(capture_switch,pigpio.PUD_UP)

# Defining functions for putting off each LED
def normalON():
    # orangeyellow is ON and the other is OFF
    pi.write(led_top,0)
    pi.write(led_bottom,1)

def secondaryON():
    # toggle
    pi.write(led_top,1)
    pi.write(led_bottom,0)

normalON()


camera=picamera.PiCamera() 

camera.framerate=15

camera.resolution= camera.MAX_IMAGE_RESOLUTION
camera.vflip=True

time.sleep(0.1)
try:
    while True:
        stream=io.BytesIO()
        camera.start_preview()
        pi.wait_for_edge(capture_switch,pigpio.RISING_EDGE)
    
        t1=cv2.getTickCount()
        camera.capture(stream,format='jpeg',use_video_port=True)


        image1=np.fromstring(stream.getvalue(),dtype=np.uint8)
        stream.truncate()
        #secondaryON()
        camera.capture(stream,format='jpeg',use_video_port=True)
        
        image2=np.fromstring(stream.getvalue(),dtype=np.uint8)
        t2=cv2.getTickCount()
        stream.truncate()
        time_taken=(t2-t1)/cv2.getTickFrequency()
        print "files captured time taken:"+str(time_taken)
        image1=cv2.imdecode(image1,1)
        image2=cv2.imdecode(image2,1)
        camera.stop_preview()
        name=raw_input("enter the name to be saved")
        
        
        cv2.imwrite('images/test/' + name + '.jpg',image1)
        
        cv2.imwrite('images/image' + str(i) + '_2.jpg',image2)
        t3=cv2.getTickCount()
        time_taken=(t3-t1)/cv2.getTickFrequency()
        print "files saved time taken:"+str(time_taken)
        i=i+1
        normalON()
        
            
except KeyboardInterrupt:
    print 'Interrupted'
    normalON()
    camera.stop_preview()
    pi.stop()

        
            

    

