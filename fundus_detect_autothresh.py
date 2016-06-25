import cv2
import numpy as np
import imutils

loc='C:/Users/Ebin/Desktop/owl/test/'

name='Sandeep4.jpg'
img2 = cv2.imread(loc+name)
img=imutils.resize(img2,width=432,height=324)
#img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#cimg = cv2.medianBlur(cimg,5)
cv2.imshow('image',img)
#cv2.waitKey(5000)

circles = cv2.HoughCircles(cimg, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 200)

if circles is not None:
    print "no circles found"
    center=(1500,968)
    radius=828
else:
    
    circles = np.uint16(np.around(circles))

    for i in circles[0,:]:
        # draw the outer circle
        image=img.copy()
        center=(i[0],i[1])
        radius=i[2]
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

    center=(center[0]*6,center[1]*6)
    radius=radius*6
    print center
    print radius
mask=np.zeros(img2.shape[:], dtype=np.uint8)
#mask=np.uint8(mask)
cv2.circle(mask,center,radius,(255,255,255),thickness=-1)
#mask=mask[:,:,1]
mask=cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)

ret,mask=cv2.threshold(mask,10,1,cv2.THRESH_BINARY)
b=np.multiply(img2[:,:,0],mask)
g=np.multiply(img2[:,:,1],mask)
r=np.multiply(img2[:,:,2],mask)
img_final=np.zeros(img2.shape[:])
img_final=np.uint8(img_final)
img_final[:,:,0]=b
img_final[:,:,1]=g
img_final[:,:,2]=r

print "done with part1"

mask=cv2.cvtColor(img_final,cv2.COLOR_BGR2GRAY)
ret,mask=cv2.threshold(mask,100,255,cv2.THRESH_BINARY_INV)
circles = cv2.HoughCircles(mask, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 200)
circles = np.uint16(np.around(circles))
print 'done'
for i in circles[0,:]:
        # draw the outer circle
##        image=img.copy()
##        center=(i[0],i[1])
##        radius=i[2]
        cv2.circle(mask,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(mask,(i[0],i[1]),2,(0,0,255),3)

b=np.multiply(img_final[:,:,0],mask)
g=np.multiply(img_final[:,:,1],mask)
r=np.multiply(img_final[:,:,2],mask)
img_final=np.zeros(img2.shape[:])
img_final=np.uint8(img_final)
img_final[:,:,0]=b
img_final[:,:,1]=g
img_final[:,:,2]=r

mask=imutils.resize(mask,width=648)
filtered=imutils.resize(img_final,width=648)
# cv2.imshow('detected circles',img)
cv2.imshow('mask',mask)
cv2.imshow('filtered',filtered)
cv2.imwrite(loc+'processed/'+name,img_final)
cv2.waitKey(0)
cv2.destroyAllWindows()
