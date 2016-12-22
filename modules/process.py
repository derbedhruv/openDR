## The entire python pipeline to process the image
import cv2
import sys
sys.path.insert(0, '/home/pi/openDR/modules/') 
from extract import extract_fundus
import remove_glare
import theia

## TODO:
## ------------
## 1. Image parameters (center x,y, radius) should be arguments
'''2. DONE--<Can integrate all functions into single module '''
## 3. Image file should go as an argument and processed image returned, i.e.
##    this file should also be converted to a module

def grade(filename):
    output = filename[:-4] + '_processed.jpg'
    cv2.imwrite(output, remove_glare.remove_glare(extract_fundus(filename)))
    return theia.grade_request(output)
