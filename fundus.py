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
import RPi.GPIO as GPIO

# set the pins - names are based on the colours of the wires connecting to the LEDs
# NOTE: Both the orangeyellow and bluegreen LEDs are active LOW, hence False is ON and vice versa
orangeyellow = 14
bluegreen  = 15
switch = 18
i=1	# initial_counter

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(orangeyellow ,GPIO.OUT)
GPIO.setup(bluegreen, GPIO.OUT)

# Defining functions for putting off each LED
def normalON():
    # orangeyellow is ON and the other is OFF
    GPIO.output(orangeyellow, False)
    GPIO.output(bluegreen, True)

def secondaryON():
    # toggle
    GPIO.output(orangeyellow, True)
    GPIO.output(bluegreen, False)
    
# Begin the polling for the switch
normalON()

with picamera.PiCamera() as camera:
    camera.resolution = (2592,1944);
    try:
        while True:
             filename = 'images/image',i,'.jpg'
             camera.start_preview()
             GPIO.wait_for_edge(switch,GPIO.RISING)
            
	     # Button is pressed
             # First capture a picture with the first LED on
             camera.capture('images/image' + str(i) + '_1.jpg', use_video_port=True)

             # Then capture with the second LED
             secondaryON() 
             camera.capture('images/image' + str(i) + '_2.jpg', use_video_port=True)

	     # Reset LED states
             normalON()
             camera.stop_preview()
             i=i+1
    except  KeyboardInterrupt: 
    #    except ValueError:
    
        print "Interrupted"
        GPIO.output(orangeyellow, False)
        GPIO.output(bluegreen, True)
        GPIO.cleanup()
