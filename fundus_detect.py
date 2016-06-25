import cv2
import numpy as np
import imutils

# stores location of the images
# make sure to create a new directory called "processed" in the path directory
# reason given at the end
path='C:/Users/Ebin/Desktop/owl/test/'

# name of the image
name='Sandeep4.jpg'

# read the image file and resize it for processing
# (432,324)is chosen since it is 1/6th the max image resolution.
# will help in further steps
# img2 is the true image, img2 the resized one we work with
img2 = cv2.imread(path+name)
img=imutils.resize(img2,width=432,height=324)
##img = cv2.medianBlur(img,5)

# HoughCircles() need Grayscale images
##cimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# to show the loaded image
cv2.imshow('image',img)

#for debugging purposes
##cv2.waitKey(5000)

#to detect circles in the image
circles = cv2.HoughCircles(cimg, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 200)

# initially it checked if circle is none, but was modified to use the hard-coded
# center and radius values at all times
# it was meant to check for circles, if none are found, use the hardcoded values
if circles is not None:
#    print "no circles found"
    center=(1500,968)
    radius=828
else:
    # to get the detected circles as numpy array
    circles = np.uint16(np.around(circles))

    for i in circles[0,:]:
        # draw the outer circle
        image=img.copy()
        center=(i[0],i[1])
        radius=i[2]
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

    #to calculate the circle for the true image from the resized one
    center=(center[0]*6,center[1]*6)
    radius=radius*6
    print center
    print radius

# to make a mask for extracting the fundus, using the center and radius obtained
# mask is the same size as the original image
# mask is an np array of type uint8, for use in OpenCV functions
mask=np.zeros(img2.shape[:], dtype=np.uint8)
cv2.circle(mask,center,radius,(255,255,255),thickness=-1)

# the mask will be a bgr image
# has to be converted to grayscale for threshholding
mask=cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)

# threshholding the grayscale image to get a binary image, with max_value 1
ret,mask=cv2.threshold(mask,10,1,cv2.THRESH_BINARY)

# the mask is multiplied with all 3 channels of the original image 
b=np.multiply(img2[:,:,0],mask)
g=np.multiply(img2[:,:,1],mask)
r=np.multiply(img2[:,:,2],mask)

# img_final combines these 3 seperated channels to get the final Fundus image
img_final=np.zeros(img2.shape[:])
img_final=np.uint8(img_final)
img_final[:,:,0]=b
img_final[:,:,1]=g
img_final[:,:,2]=r

# the mask and final image are resized for displaying on screen
mask=imutils.resize(mask,width=648)
filtered=imutils.resize(img_final,width=648)

# cv2.imshow('detected circles',img)
#cv2.imshow('mask',mask)
cv2.imshow('filtered',filtered)

# the processed images are stored in a new folder called "processed" in the given path 
cv2.imwrite(loc+'processed/'+name,img_final)

cv2.waitKey(0)
cv2.destroyAllWindows()
