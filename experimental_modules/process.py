## The entire python pipeline to process the image
import cv2
import fundus
import remove_glare
import theia

## TODO:
## ------------
## 1. Image parameters (center x,y, radius) should be arguments
## 2. Can integrate all functions into single module
## 3. Image file should go as an argument and processed image returned, i.e.
##    this file should also be converted to a module

# process.py should be called on every image taken
filename = 'test.jpg'
output = "out.jpg"

cv2.imwrite(output, remove_glare.remove_glare(fundus.extract_fundus(filename)))
print theia.grade_request(open(output))
