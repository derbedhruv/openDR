                        #############################
                        ## Fundus_Cam.py           ##
                        ## Primary Author: Ebin    ##
                        ## Version : 1.0           ##
			##Contributor: Ayush Yadav ##
                        #############################


from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
import numpy as np
import io

#########################################################################
# This class provide access to the picamera and its associated functions#
#########################################################################

class Fundus_Cam(object):

    # The constructor initializes the camera object and starts preview
    def __init__(self, framerate=12,preview=False):

        # initialize the camera 
        self.camera = PiCamera()
        self.camera.resolution = self.camera.MAX_IMAGE_RESOLUTION
        self.camera.framerate = framerate

        # stream is a file-like type used to store captured images to memory
        # rather than onto disk
        self.stream = io.BytesIO()

        # this determines the vertical flip_state of the picamera
        # this can be toggled by Fundus_Cam.flip_cam()
        self.flip_state=False
        
        # This is a list to store images captured in Fundus_Cam.continuous_capture()
        self.images=[]
        self.camera.start_preview()

        # used to stop and start recording in versions higher than1.0
        self.stopped = False

    def continuous_capture(self):
        # starts a new thread, which runs the update()
        self.stopped = False
        Thread(target=self.update, args=()).start()
        

    # continuosly captures frames from the camera, in a seperate thread
    def update(self):
        # keep looping infinitely until the thread is stopped
        # In version 1.0 it grabs only 10 frames
        while True:
                # grab the frame from the stream 
                self.camera.capture(self.stream,format='jpeg',use_video_port=True)
                # convert the frame captures to numpy array and append to images
                self.images.append(np.fromstring(self.stream.getvalue(),dtype=np.uint8))
                # clear the stream for the next frame
                self.stream.truncate()
                self.stream.seek(0)
                if(len(self.images)>9):
                    self.stopped=True
                    return
                
    
    # to flip the camera 
    def flip_cam(self):
        self.camera.vflip=(not self.flip_state)

    #to capture a single image
    def capture(self):
        self.camera.capture(self.stream,format='jpeg',use_video_port=True)
        # convert to numpy array
        self.image=np.fromstring(self.stream.getvalue(),dtype=np.uint8)
        # clear the stream
        self.stream.truncate()
        self.stream.seek(0)
        # return the captured image
        return self.image

    # to start camera preview
    def preview(self):
        self.camera.start_preview()

    # to stop camera preview
    def stop_preview(self):
        self.camera.stop_preview()

    # used in version higher than 1.0
    def stop(self):
        self.stopped=True

    def __del__(self):
        camera.close()

##    def decode_image(images,path_sen,name):
##    #name=raw_input("enter the name to be saved")
##        no=1
##        if type(images) is list:
##        
##            for img in images:
##                image=cv2.imdecode(img,1)
##                #image=get_fundus(image)
##                cv2.imwrite(path_sen + name + '_'+str(no)+'.jpg',image)
##                no=no+1
##        else:
##            image=cv2.imdecode(images,1)
##            #image=get_fundus(image)
##            cv2.imwrite(path_sen + name + '.jpg',image)   
   
######        End of Class Implementation  ############
#######################################################

    
        

# decode,process and save the grabbed image

            
        

# for debugging
if __name__=='__main__':
    
    fundus_cam=Fundus_Cam()
    ## this part of the code is for debugging and testing the Fundus_Cam class
    image=fundus_cam.capture()
    raw_input("start continuous??")
    fundus_cam.continuous_capture()
    while not fundus_cam.stopped:
        pass
    print "decoding still"
    decode_image(image)
    print "decoding continuous capture"
    decode_image(fundus_cam.images)
    fundus_cam.stop_preview()
    
    
        
    

    
