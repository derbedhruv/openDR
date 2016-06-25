##################################################################
##  OWL v2.7					                        		##
## ------------------------------------------------------------ ##
##  Primary Author: Dhruv Joshi                                 ##
##  Srujana Center for Innovation, LV Prasad Eye Institute	    ##
##  								                            ##
##  This code will wait for an external button press, capture	##
##  two images in rapid succession with two different white  	##
##  LEDs, process them to remove glare computationally, send	##
##  them to the theia algo backend to be processed, save them	##
##  and return the score on-screen in human readable format.	##
##                                                              ##        
##  Code Contributors: Ayush Yadav, Devesh Jain, Ebin Philip    ##
##                                                              ##
##  New in 2.6 :  Path corrected and Onscreen keyboard added    ##
##################################################################

import time
import picamera
import pigpio
import os
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, session, g, url_for, flash

from flask import Response
from Fundus_Cam import Fundus_Cam



#-------------------Flask implementation starts here--------------------#


#create flask app
app = Flask(__name__)

#URL setter
@app.route('/')
def my_form():
    return render_template("index.html")

#MR number input is accepted here
@app.route('/', methods=['POST'])
def my_form_post():
    global processed_text
    global obj_state
    obj_state = True
    text = request.form['text']
    processed_text = text.upper()
    make_a_dir(processed_text)
    obj_fc = Fundus_Cam()
    return redirect(url_for('captureSimpleFunc'))

##@app.route('/captureSimple')
##def loadSimple():
##    return render_template('capture_simple.html')    

#captureSimple : to displey simple image    
@app.route('/captureSimple', methods=['GET','POST'])
def captureSimpleFunc():
    if request.method == 'GET':
        return render_template('capture_simple.html')
    if request.method == 'POST':
        #If flip button pressed
        if request.form['Flip']=='Flip':
            obj_fc.flip-cam()
            #return render_template('capture_simple.html')
    
        #if 'Click' button pressed
        if request.form['Click']=='Click' :
            obj_fc.capture()
            Fundus_Cam.decode_images(obj_fc.image,os.path.dirname(__file__)+"/images/"+processed_text,'xyz1.jpg')
        

        #if 'Video' has to be taken and 'Vid' button is pressed
        if request.form['Vid']=='Vid':
            obj_fc.continuous_capture()
            #return render_template('capture_simple.html')
        
        #if stop button is pressed
        if request.form['stop']=='stop':
     	    if obj_state == True:
                obj_fc.stop_preview()
                obj_fc.stop()
                obj_state=False
    	    else:
                obj_fc.Fundus_Cam()
                obj_state==True

        return render_template('capture_simple.html')
        if request.form['shutd']=='shutd':
            os.system("shutdown now -h")
        #return render_template('capture_simple.html')
    
    
#Cam flask routes -----------------------#-------------------------------

#@app.route('/video_feed')
#def video_feed():
#    return Response(gen(Fundus_Cam()),
#                    mimetype='multipart/x-mixed-replace; boundary=frame')
#
#def gen(Fundus_Cam):
#    while True:
#        frame = Fundus_Cam.get_frame()
#        yield (b'--frame\r\n'
#               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


#main--------------------#

if __name__ == '__main__':
    app.run()






#..........Below this line, all the functions not having flask lie.........#


#make a directory of patient's name if it does not exist
def make_a_dir(pr_t):
    d= os.path.dirname(__file__)+"/images/"+pr_t
    if not os.path.exists(d):
        os.mkdir(d)
    


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
    


#function for capturing HQ images
##def take_a_pic(pr_tx):    
##    camera.capture('images/'+pr_tx+'/' + str(i) + '_1.jpg', use_video_port=False)
##
## # Then capture with the second LED
##    secondaryON() 
##    camera.capture('images/'+pr_tx+'/' + str(i) + '_2.jpg', use_video_port=False)
##    
## # Reset LED states
##    normalON()
##    camera.stop_preview()
##    i=i+1
##




# Begin the polling for the switch
##def fundusRun(pr_t):
##    normalON()
##    
##    with picamera.PiCamera() as camera:
##        camera.resolution =  camera.MAX_IMAGE_RESOLUTION
##        try:
##        
##            while True:
##                    #filename = 'images/image',i,'.jpg'
##                    #camera.start_preview()
##                    camera.vflip = False
##                    time.sleep(0.01)
##                    pi.wait_for_edge(switch,pigpio.RISING_EDGE)
##                    take_a_pic(pr_t)
##                 # Button is pressed
##                 # First capture a picture with the first LED on
##                 # use_video_port=False enables capturing the image using the STILL port giving max resolution, instead of the video port. DO NOT CHANGE.
##                    
##                    
##                 #    camera.capture('images/'+pr_t+'/' + str(i) + '_1.jpg', use_video_port=False)
##
##                 # # Then capture with the second LED
##                 #    secondaryON() 
##                 #    camera.capture('images/'+pr_t+'/' + str(i) + '_2.jpg', use_video_port=False)
##    
##                 # # Reset LED states
##                 #    normalON()
##                 #    camera.stop_preview()
##                 #    i=i+1
##        except  KeyboardInterrupt: 
##        #   except ValueError:
##            print 'Interrupted'
##            pi.write(orangeyellow,0)
##            pi.write(bluegreen,0)
##            camera.stop_preview()
##            pi.stop()
