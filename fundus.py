##################################################################
##  OWL v2.6					                ##      		##
## ------------------------------------------------------------ ##
##  Primary Author: Dhruv Joshi                                 ##
##  Srujana Center for Innovation, LV Prasad Eye Institute	##
##  								##                            ##
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
# from camerax import VideoCamera
from flask import Response
from Fundus_Cam import Fundus_Cam

###################### Taken from fundus-mod2-- Remove comment if it works
import io
import cv2
from picamera.array import PiRGBArray
#######################



#-------------------Flask implementation starts here--------------------#

#create flask app
app = Flask(__name__)

#URL setter
@app.route('/')
def my_form():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():
    global processed_text
    text = request.form['text']
    processed_text = text.upper()
    make_a_dir(processed_text)#sends data for foldername to make_a_dir()
    return redirect(url_for('captureSimpleFunc'))
    #fundusRun(processed_text)
    



#captureSimple : to displey simple image    
@app.route('/captureSimple', methods=['GET'])
def captureSimpleFunc():
    return render_template("capture_simple.html")
    fundusRun(processed_text)
    if request.form(['flip']) == 'Flip' :
        #Run command to flip the output
        camera.vflip = not camera.vflip;
        return redirect(url_for('captureSimpleFunc'))

    elif request.form(['click_pic']) == 'Capture':
        #Run Function toggle capture image
        take_a_pic(processed_text)
        return redirect(url_for('captureSimpleFunc'))
        
    else:
        return redirect(url_for('captureSimpleFunc'))


#--Cam flask routes --------------------#-------------------------------

@app.route('/video_feed')
def video_feed():
    return Response(gen(Fundus_Cam()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(Fundus_Cam):
    while True:
        frame = Fundus_Cam.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


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
#The below comment has to be corrected by Ebin
# NOTE: Both the orangeyellow and bluegreen LEDs are active LOW, hence 0 is ON and vice versa
camera=picamera.PiCamera() 

led_top=2
led_bottom=3
capture_switch=4
i=1	# initial_counter

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


###--Next function commented because it's elements have been included in fundusRun() fuction
# #function for capturing HQ images
# def take_a_pic(pr_tx):  
#     #An external file named 'name' stores a key for the number of times the capture button has been clicked
#     #This helps in naming the files as the value is read and appended to image name
#     #This also removes any sort of problem which can ever be caused in naming 
#     #This method is foolproof


#     #read file  
#     filer = open('name','r')
#     picn = (int)(filer.read())
#     picn = picn+1
#     filer.close()

#     #increment the iteration key in file
#     filew = open('name','w')
#     filew.write(str(picn))
#     filew.close()

#     camera.capture('images/'+pr_tx+'/'+ str(picn) + '_' + str(i) + '_1.jpg', use_video_port=False)

#  # Then capture with the second LED
#     secondaryON() 
#     camera.capture('images/'+pr_tx+'/' + str(picn) + '_' + str(i) + '_2.jpg', use_video_port=False)
    
#  # Reset LED states
#     normalON()
#     camera.stop_preview()
#     i=i+1





# Begin the polling for the switch
def fundusRun(pr_t):
    normalON()
    #with picamera.PiCamera() as camera:
        camera.resolution =  camera.MAX_IMAGE_RESOLUTION
        try:
        
            while True:
                    #filename = 'images/image',i,'.jpg'
                    #camera.start_preview()
                    camera.vflip = False
                    time.sleep(0.01)
                    stream=io.BytesIO()
                    camera.start_preview()
                    pi.wait_for_edge(switch,pigpio.RISING_EDGE)


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
                    #name=raw_input("enter the name to be saved")

                    #An external file named 'name' stores a key for the number of times the capture button has been clicked
                    #This helps in naming the files as the value is read and appended to image name
                    #This also removes any sort of problem which can ever be caused in naming 
                    #This method is foolproof

                    #read file  
                    filer = open('name','r')
                    picn = (int)(filer.read())
                    picn = picn+1
                    filer.close()

                    #increment the iteration key in file
                    filew = open('name','w')
                    filew.write(str(picn))
                    filew.close()

                    cv2.imwrite('images/'+pr_tx+'/'+ str(picn) + '_' + str(i) + '_1.jpg',image1)
                    cv2.imwrite('images/'+pr_tx+'/'+ str(picn) + '_' + str(i) + '_2.jpg',image2)
                    t3=cv2.getTickCount()
                    time_taken=(t3-t1)/cv2.getTickFrequency()
                    print "files saved time taken:"+str(time_taken)

                    #camera.capture('images/'+pr_tx+'/'+ str(picn) + '_' + str(i) + '_1.jpg', use_video_port=False)

                    # Then capture with the second LED
                    #secondaryON() 
                    #camera.capture('images/'+pr_tx+'/' + str(picn) + '_' + str(i) + '_2.jpg', use_video_port=False)
                    
                    # Reset LED states
                    normalON()
                    camera.stop_preview()
                    i=i+1
        except  KeyboardInterrupt: 
        #   except ValueError:
            print 'Interrupted'
            camera.stop_preview()
            pi.stop()
