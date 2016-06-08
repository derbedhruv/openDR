from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2

class Fundus_Cam(object):
    def __init__(self, resolution=(320, 240), framerate=32,preview=False):
        # initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,format="bgr", use_video_port=True)
        self.preview=preview
        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.stopped = False
        self.key=0

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
                # grab the frame from the stream and clear the stream in
                # preparation for the next frame
                self.frame = f.array
                if self.preview:
                    cv2.imshow('window', self.frame)
                    self.key=cv2.waitKey(1)
                self.rawCapture.truncate(0)


                # if the thread indicator variable is set, stop the thread
                # and resource camera resources
                if self.stopped:
                        cv2.destroyAllWindows()
                        self.stream.close()
                        self.rawCapture.close()
                        self.camera.close()
                        return

    def read(self):
        return self.frame

    def capture_image(self,name,no):
        self.camera.capture('images/image' + str(name) + '_'+str(no)+'.jpg', use_video_port=False)
        

    def get_frame(self):
        self.ret, self.jpeg = cv2.imencode('.jpg', self.frame)
        return self.jpeg.tobytes()
    
    def stop(self):
        self.stopped=True

if __name__=='__main__':
    
   fundus_cam=Fundus_Cam((640,480),15,True).start()
   
    
