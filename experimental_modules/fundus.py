import cv2
import numpy as np
import imutils

# constants for extract_circles()
center=(1386,948)
radius=804

# constants for erode_thresh()
threshold_value=65          # emperical
kernel_size=14
erosion_iterations=5


#function to extract circular region from the given image
def extract_circles(image):

    #make a zeros matrix of same dimension as image
    mask=np.zeros(image.shape[:], dtype=np.uint8)

    #draw a white circle in the mask
    cv2.circle(mask,center,radius,(255,255,255),thickness=-1)

    # the mask will be a bgr image
    # has to be converted to grayscale for threshholding
    mask=cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)


    # threshholding the grayscale image to get a binary image, with max_value 1
    ret,mask=cv2.threshold(mask,10,1,cv2.THRESH_BINARY)

    # the mask is multiplied with all 3 channels of the original image 
    b=np.multiply(image[:,:,0],mask)
    g=np.multiply(image[:,:,1],mask)
    r=np.multiply(image[:,:,2],mask)

    # img_final combines these 3 seperated channels to get the final Fundus image
    img_final=np.zeros(image.shape[:])
    img_final=np.uint8(img_final)
    img_final[:,:,0]=b
    img_final[:,:,1]=g
    img_final[:,:,2]=r

    return img_final

# function to erode and threshold a given image
def erode_thresh(image):

    image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    #kernel for erosion
    kernel=np.ones((kernel_size,kernel_size),np.uint8)

    #threshold the image 
    ret,threshed=cv2.threshold(image,threshold_value,255,cv2.THRESH_BINARY)
    
    #erode the thresholded image to smoothen the edges
    threshed=cv2.erode(threshed,kernel,iterations = erosion_iterations)

    #blur the image to smoothen it
    cv2.GaussianBlur(threshed,(21,21),0)

    return threshed


# function to fit an ellipse, given an image and its thresholded form
def ellipse_fit(image,cont_img):
    # to detect contours in the binary image
    contours, hierarchy = cv2.findContours(cont_img, cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)

    # make a mask of zeros
    mask=np.zeros(image.shape[:], dtype=np.uint8)

    # find the biggest contour and fit an ellipse
    c=max(contours, key=cv2.contourArea)
    ellipse = cv2.fitEllipse(c)

    # draw an ellipse of the same size on the mask
    cv2.ellipse(mask, ellipse, (255,255,255), -1)


    # the mask will be a bgr image
    # has to be converted to grayscale for threshholding
    mask=cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)

    # threshholding the grayscale image to get a binary image, with max_value 1
    ret,mask=cv2.threshold(mask,10,1,cv2.THRESH_BINARY)

    # the mask is multiplied with all 3 channels of the original image 
    b=np.multiply(image[:,:,0],mask)
    g=np.multiply(image[:,:,1],mask)
    r=np.multiply(image[:,:,2],mask)

    # img_final combines these 3 seperated channels to get the final Fundus image
    img_final=np.zeros(image.shape[:])
    img_final=np.uint8(img_final)
    img_final[:,:,0]=b
    img_final[:,:,1]=g
    img_final[:,:,2]=r

    return img_final

## Combining these functions into one simple, importable function
# Will take image (filename) as arg and return extracted numpy array
def extract_fundus(filename):
    test_img=cv2.imread(filename)
    circle=extract_circles(test_img)
    threshed_image=erode_thresh(circle)
    return ellipse_fit(circle,threshed_image)
    
