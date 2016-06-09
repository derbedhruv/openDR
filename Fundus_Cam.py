from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
import numpy as np

class Fundus_Cam(object):
    def __init__(self, resolution=(320, 240), framerate=32,preview=False):
        # initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,format="bgr", use_video_port=True)
    
       # initialize self.frame by grabbing one frame from the camera 
        
        for f in self.stream:
                # grab the frame from the stream and clear the stream in
                # preparation for the next frame
                self.frame = f.array
                self.rawCapture.truncate(0)
                break
            
        self.stopped = False

    def start(self):
        # starts a new thread, which runs the update()
        Thread(target=self.update, args=()).start()
        return self

    # continuosly grabs frames from the camera, in a seperate thread
    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
                # grab the frame from the stream and clear the stream in
                # preparation for the next frame
                self.frame = f.array
                self.rawCapture.truncate(0)

                # if the thread indicator variable is set, stop the thread
                # and resource camera resources
                if self.stopped:
                        #cv2.destroyAllWindows()
                        self.stream.close()
                        self.rawCapture.close()
                        self.camera.close()
                        return
    # to return the last grabbed frame
    def read(self):
        return self.frame

    #to capture and store images 
    def capture_image(self,name,no):
        self.camera.capture('images/image' + str(name) + '_'+str(no)+'.jpg', use_video_port=False)
        

    #returns the last grabbed frame in JPEG
    def get_frame(self):
        
        self.ret, self.jpeg = cv2.imencode('.jpg', self.frame)
        return self.jpeg.tobytes()
    
    def stop(self):
        self.stopped=True

if __name__=='__main__':
    
    fundus_cam=Fundus_Cam((640,480),32,True).start()
    ## this part of the code is for debugging and testing the Fundus_Cam class
    while True:
       image=fundus_cam.read()
       cv2.imshow('window',image)
       key=cv2.waitKey(1)
       if key==27:
           break
    fundus_cam.stop()
    cv2.destroyAllWindows()

    
