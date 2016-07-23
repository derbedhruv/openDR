##################################################################
##  OWL v2.9					                        		##
## ------------------------------------------------------------ ##
##  Authors: Ayush Yadav, Devesh Jain, Ebin Philip, Dhruv Joshi ##
##  Srujana Center for Innovation, LV Prasad Eye Institute	    ##
##  								                            ##
##  This code will wait for an external button press, capture	##
##  two images in rapid succession with two different white  	##
##  LEDs, process them to remove glare computationally, send	##
##  them to the theia algo backend to be processed, save them	##
##  and return the score on-screen in human readable format.	##
##                                                              ##      
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
import cv2
import numpy as np


try:

    #-------------------Flask implementation starts here--------------------#


    #create flask app
    app = Flask(__name__)

    tokens=['Flip','Vid','Click','Switch','Shut']

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
        global obj_fc
        obj_fc = Fundus_Cam()
        return redirect(url_for('captureSimpleFunc'))

    ##@app.route('/captureSimple')
    ##def loadSimple():
    ##    return render_template('capture_simple.html')    

    #captureSimple : to displey simple image    
    @app.route('/captureSimple', methods=['GET','POST'])
    def captureSimpleFunc():
        if request.method == 'GET':
            return render_template('capture_simple.html',params=tokens)
        if request.method == 'POST':
            if "d" in request.form.keys():
                d=request.form['d']
                #if photo has to be taken
                if d == 'Click':
                    obj_fc.capture()
                    decode_image(obj_fc.image)
                    return render_template('capture_simple.html',params=tokens)


                #If flip button pressed
                if d == 'Flip':
                    obj_fc.flip_cam()
                    return render_template('capture_simple.html',params=tokens)
        
                

                #if 'Video' has to be taken and 'Vid' button is pressed
                if d=='Vid':
                    obj_fc.continuous_capture()
                    decode_image(obj_fc.images)
                    return render_template('capture_simple.html',params=tokens)
            
                #if stop button is pressed
                if d=='Switch':
                    if obj_state == True:
                        obj_fc.stop_preview()
                        obj_fc.stop()
                        return redirect(url_for('my_form'))
                        

                    return render_template('capture_simple.html',params=tokens)
                if d=='Shut':
                    shut_down()
                    return render_template('capture_simple.html',params=tokens)
        
    def decode_image(images):
        #name=raw_input("enter the name to be saved")
            global no
            no=1

            file_r = open(os.path.dirname(__name__)+'name','r')
            picn = (int)(file_r.read())
            picn = picn+1
            file_r.close()
            file_w = open(os.path.dirname(__name__)+'name','w')
            file_w.write(str(picn))
            file_w.close()
            if type(images) is list:
            
                for img in images:
                    image=cv2.imdecode(img,1)
                    #image=get_fundus(image)
                    cv2.imwrite(os.path.dirname(__file__)+"/images/" + processed_text + '/' + processed_text+ '_' + str(picn) +'_' + str(no) + '.jpg',image)
                    no=no+1
            else:
                image=cv2.imdecode(images,1)
                #image=get_fundus(image)
                cv2.imwrite(os.path.dirname(__file__)+"/images/" + processed_text + '/' + processed_text +'_' + str(picn) +'_' + str(no) + '.jpg',image)  
		no=no+1
    #-------------------Flask implementation starts here--------------------#








    #..........Below this line, all the functions not having flask lie.........#


    #make a directory of patient's name if it does not exist
    def make_a_dir(pr_t):
        d= os.path.dirname(__file__)+"/images/"+pr_t
        if not os.path.exists(d):
            os.mkdir(d)
        
    # def file_path(pr_t):
    #     fi_x=open(os.path.dirname(__file__)+'/name','r')
    #     nam = (int)(fi_x.read())+1
    #     fi_x=open(os.path.dirname(__file__)+'/name','w')
    #     fi_x.write(str(nam-1))
    #     fullpath=os.path.dirname(__file__)+"/images/"+pr_t + "/" +str(nam-1)
    #     return fullpath

        
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
except:
    render_template('''<html><body>Error occured: We will now shut down</body></html>''')
    time.sleep(3)
    shut_down()


def shut_down():
        command = "/usr/bin/sudo /sbin/shutdown now"
        import subprocess
        process=subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output    
    
if __name__ == '__main__':
    app.run()
