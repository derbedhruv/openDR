##################################################################
##  The primary code which will be run by a deamon on the rPI	##
##  OWL v2.1							##
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
orangeyellow = 14	# NOTE: this pin is active LOW, hence FALSE is ON
bluegreen  = 15
switch = 18
i=1	# initial_counter

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(orangeyellow ,GPIO.OUT)
GPIO.setup(bluegreen, GPIO.OUT)

# setting white ON but IR off
GPIO.output(orangeyellow, False)
GPIO.output(bluegreen, False)

with picamera.PiCamera() as camera:
    camera.resolution = (2592,1944);
    try:
        while True:
             filename = 'images/image',i,'.jpg'
             camera.start_preview()
             GPIO.wait_for_edge(switch,GPIO.RISING)
            
	    # Button is pressed
             GPIO.output(bluegreen, True)
             GPIO.output(orangeyellow, False)
             camera.capture('images/image'+str(i)+'.jpg',use_video_port=True)

	    #Set the white LED OFF
             GPIO.output(orangeyellow, True)
             GPIO.output(bluegreen, False)
             camera.stop_preview()
             i=i+1
    except  KeyboardInterrupt: 
    #    except ValueError:
    
        print "Interrupted"
        GPIO.output(orangeyellow, False)
        GPIO.output(bluegreen, True)
        GPIO.cleanup()
