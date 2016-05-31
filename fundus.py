##################################################################
##  OWL v2.1							##
## ------------------------------------------------------------ ##
##  Primary Author: Dhruv Joshi
##  Srujana Center for Innovation, LV Prasad Eye Institute	##
##  								##
##  This code will wait for an external button press, capture	##
##  two images in rapid succession with two different white  	##
##  LEDs, process them to remove glare computationally, send	##
##  them to the theia algo backend to be processed, save them	##
##  and return the score on-screen in human readable format.	##
##								##
##################################################################

import time
import picamera
import pigpio

# set the pins - names are based on the colours of the wires connecting to the LEDs
# NOTE: Both the orangeyellow and bluegreen LEDs are active LOW, hence 0 is ON and vice versa
orangeyellow = 2
bluegreen  = 3
switch = 4
i=1	# initial_counter

# pi is initialized as the pigpio object
pi=pigpio.pi()

pi.set_mode(orangeyellow,pigpio.OUTPUT)
pi.set_mode(bluegreen,pigpio.OUTPUT)
pi.set_mode(switch,pigpio.INPUT)
#set a pull-up resistor on the switch pin
pi.set_pull_up_down(switch,pigpio.PUD_UP)
# Defining functions for putting off each LED
def normalON():
    # orangeyellow is ON and the other is OFF
    pi.write(orangeyellow,0)
    pi.write(bluegreen,1)

def secondaryON():
    # toggle
    pi.write(orangeyellow,1)
    pi.write(bluegreen,0)
    
# Begin the polling for the switch
normalON()
with picamera.PiCamera() as camera:
    camera.resolution =  camera.MAX_IMAGE_RESOLUTION
    try:
        
        while True:
                filename = 'images/image',i,'.jpg'
                camera.start_preview()
                time.sleep(0.01)
                pi.wait_for_edge(switch,pigpio.RISING_EDGE)
             
             # Button is pressed
             # First capture a picture with the first LED on
             # use_video_port=False enables capturing the image using the STILL port giving max resolution, instead of the video port. DO NOT CHANGE.
                camera.capture('images/image' + str(i) + '_1.jpg', use_video_port=False)

             # Then capture with the second LED
                secondaryON() 
                camera.capture('images/image' + str(i) + '_2.jpg', use_video_port=False)

             # Reset LED states
                normalON()
                camera.stop_preview()
                i=i+1
    except  KeyboardInterrupt: 
    #    except ValueError:
        print 'Interrupted'
        pi.write(orangeyellow,0)
        pi.write(bluegreen,0)
	camera.stop_preview()
	pi.stop()
