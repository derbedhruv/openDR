'''
*	REMOVAL OF LED GLARE FROM RETINAL IMAGES
----------------------------------------------------
*	Author: Dhruv Joshi
*	A very simple piece of code in openCV (3.1.0 used) to remove the two direct specular reflections on the 20D lens
*	Built for OWL 1.0 (part of openDR project at Srujana Center for Innovation, LV Prasad Eye Institute, Hyderabad, India)
'''

import numpy
import cv2

# prepare mask - square of width 'w' centered at (x,y) which is the center of the bright spots
x = 1396
y = 958
w = 100
thresh = 0.9

def remove_glare(im):
   # generate binary image mask - dilated circles around the saturated bright spots at the center
    temp = im[y-w:y+w, x-w:x+w,1]  # single channel
    ret, temp_mask = cv2.threshold(temp, thresh*256, 255, cv2.THRESH_BINARY)
    kernel = numpy.ones((25,25), 'uint8')
    temp_mask = cv2.dilate(temp_mask, kernel)

    # perform the inpainting...
    im[y-w:y+w, x-w:x+w,:] = cv2.inpaint(im[y-w:y+w, x-w:x+w,:], temp_mask, 1, cv2.INPAINT_TELEA)

    # return file
    return im
