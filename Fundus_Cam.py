from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
import numpy as np
import io

class Fundus_Cam(object):
    def __init__(self, framerate=12,preview=False):
        # initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = self.camera.MAX_IMAGE_RESOLUTION
        self.camera.framerate = framerate
        self.stream = io.BytesIO()
        self.flip_state=False

        self.images=[]
        self.camera.start_preview()
        self.stopped = False

    def continuous_capture(self):
        # starts a new thread, which runs the update()
        self.stopped = False
        Thread(target=self.update, args=()).start()
        

    # continuosly grabs frames from the camera, in a seperate thread
    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
                # grab the frame from the stream and clear the stream in
                # preparation for the next frame
                self.camera.capture(self.stream,format='jpeg',use_video_port=True)
                self.images.append(np.fromstring(self.stream.getvalue(),dtype=np.uint8))
                self.stream.truncate()
                self.stream.seek(0)
                if(len(self.images)>9):
                    self.stopped=True
                    return
##                
    

    def flip_cam():
        self.camera.vflip=(not self.flip_state)

    #to capture and store images 
    def capture(self):
        self.camera.capture(self.stream,format='jpeg',use_video_port=True)
        self.image=np.fromstring(self.stream.getvalue(),dtype=np.uint8)
        self.stream.truncate()
        self.stream.seek(0)
        return self.image

    def preview(self):
        self.camera.start_preview()
    def stop_preview(self):
        self.camera.stop_preview()
    
    def stop(self):
        self.stopped=True

def decode_image(images):
    name=raw_input("enter the name to be saved")
    if type(images) is list:
        no=1
        for img in images:
            image=cv2.imdecode(img,1)
            #image=get_fundus(image)
            cv2.imwrite('images/test/' + name + '_'+str(no)+'.jpg',image)
            no=no+1
    else:
        image=cv2.imdecode(images,1)
        #image=get_fundus(image)
        cv2.imwrite('images/test/' + name + '.jpg',image)
            
        


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
    
    
        
    

    
