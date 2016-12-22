##############################################################################
##  OWL v2.9					                        		##############
## ------------------------------------------------------------ ##############
##  Authors: Ayush Yadav, Devesh Jain, Ebin Philip, Dhruv Joshi ##############
##  Srujana Center for Innovation, LV Prasad Eye Institute	    ##############
##  								                            ##############
##  This code will wait for an external button press, capture	##############
##  two images in rapid succession with two different white  	############## 
##  LEDs, process them to remove glare computationally, send	##############
##  them to the theia algo backend to be processed, save them	##############
##  and return the score on-screen in human readable format.	##############
##                                                              ##############
##                                                              ##############
##  New in 2.6 :  Path corrected and Onscreen keyboard added    ##############
##  New in 2.9 :  Cleaned up code to conform to PEP-8 guidelines##############
##############################################################################

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

# Import the modules needed for image processing and ML grading
import sys
sys.path.insert(0, '/home/pi/openDR/modules/')    

# adding modules folder to the start of python search path
import process      # our processing module
from process import grade
# since the folder locations are fixed, hard-coding filesystem locations
base_folder = '/home/pi/openDR'

#a dynamic grading key
grade_val = 'Grade'

last_img =  '1'
try:

    #-------------------Flask implementation starts here-------------------#

    #create flask app
    app = Flask(__name__)
    
    #tokens would have the value for each but
    tokens=['Flip' , 'Vid' , 'Click' , 'Switch' , grade_val , 'Shut' ]

    #URL setter
    @app.route( '/' )
    def my_form():
    	normalON()
        return render_template( "index.html" )

    #MR number input is accepted here
    @app.route('/', methods = ['POST'])
    def my_form_post():
        #processesd_text stores the MR_number
        global processed_text
        global obj_state
        global last_img
  
        obj_state = True

        #input for MR Number into 'text' variable
        text = request.form['text']
        
        #converting input text to upper case for final MR number
        processed_text = text.upper()
        make_a_dir(processed_text)
        
        #declaring object Fundus_cam
        global obj_fc
        obj_fc = Fundus_Cam()

        return redirect(url_for('captureSimpleFunc'))


    #captureSimple : to display simple image    
    @app.route('/captureSimple', methods=['GET','POST'])
    def captureSimpleFunc():
        global last_img
        global grade_val
        if request.method == 'GET':
            return render_template('capture_simple.html', params=tokens, grades={})
        if request.method == 'POST':
            if "d" in request.form.keys():
                d=request.form['d']

                #if photo has to be taken
                if d == 'Click':
                    obj_fc.capture()
                    decode_image(obj_fc.image)
                    return render_template('capture_simple.html', params=tokens, grades={})

                #If flip button pressed
                if d == 'Flip':
                    obj_fc.flip_cam()
                    return render_template('capture_simple.html', params=tokens, grades={})

                
                #if 'Video' has to be taken and 'Vid' button is pressed
                if d == 'Vid':
                    obj_fc.continuous_capture()
                    decode_image(obj_fc.images)
                    return render_template('capture_simple.html', params=tokens, grades={})

                #if photo has to be taken
                if d == grade_val:
                    if last_img == '1':
                        return render_template('capture_simple.html', params=tokens, grades={'grade':'NO IMAGE SPECIFIED'})

                    if last_img != '1':
                        # grading_val(last_img)
                        grade_val = str(grade(last_img))[:4]
                        print "the grade is " + grade_val
                        return render_template('capture_simple.html', params=tokens, grades={'grade':grade_val})


                #if stop button is pressed
                if d == 'Switch':
                    if obj_state == True:
                        obj_fc.stop_preview()
                        obj_fc.stop()
                        return redirect(url_for('my_form'))
                        
                    return render_template('capture_simple.html', params=tokens, grades={})
                if d == 'Shut':
                    shut_down()
                    return render_template('capture_simple.html', params=tokens, grades={})
    
    # A seperate function for getting the value from theia and assigning it to grade_val
    def grading_val(last_img):
        global grade_val
        grade_val = str(grade(last_img))
        print "the grade is " + grade_val
        pass


        
    def decode_image(images):
        #name=raw_input("enter the name to be saved")
            global no
            global last_img
            global grade_val
            no=1
            ## This part of code is to open the file 'name' and add the number
            #  in the file to the pic taken and increment it
            ## This is done so that each pic taken has a unique name and also no
            #  overwriting happens
            file_r = open(base_folder + '/name','r')
            picn = (int)(file_r.read())
            picn = picn+1
            file_r.close()
            file_w = open(base_folder + '/name','w')
            file_w.write(str(picn))
            file_w.close()
            last_img = (base_folder + "/images/" 
                                   + processed_text 
                                   + '/' 
                                   + processed_text 
                                   +'_' + str(picn) 
                                   + '_' + str(no) 
                                   + '.jpg')
            # Save image in the particular directory with the given file name
            if type(images) is list:
            
                for img in images:
                    image=cv2.imdecode(img,1)
                    #image=get_fundus(image)
                    cv2.imwrite( last_img, image )
                    no=no+1
            else:
                image=cv2.imdecode(images,1)
                #image=get_fundus(image)
                cv2.imwrite( last_img,image )  
		no=no+1
    #-------------------Flask implementation ends here--------------------#

    #--------------NO MAN'S LAND. ABANDON ALL HOPE YE WHO ENTER-----------#

    #......Below this line, all the functions not having flask lie.....#


    #make a directory of patient's name if it does not exist
    def make_a_dir(pr_t):
        d = base_folder + "/images/"+pr_t
        if not os.path.exists(d):
            print os.path.dirname(__file__)
            os.mkdir(d)
        
        
    # Set the pins
    # Names are based on the colours of the wires connecting to the LEDs
    # NOTE: Both the orangeyellow and bluegreen 
    #       LEDs are active LOW, hence 0 is ON and vice versa
    orangeyellow = 14
    bluegreen  = 15
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
        

#exception module not working as desired
except :
    e = sys.exc_info()[0]
    write_to_page( "<body>Error occured: We will now shut down <p>%s</p></body>" % e )
    
    #wait for 3 seconds
    time.sleep(3)
    #call shutdown function
    shut_down()

#function pipes the 'shutdown now' command to terminal
def shut_down():
        command = "/usr/bin/sudo /sbin/shutdown now"
        import subprocess
        process=subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded = True)

