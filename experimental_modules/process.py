## The entire python pipeline to process the image
import cv2
import fundus
import remove_glare
import theia

# This should go as an argument
# process.py should be called on every image taken
filename = 'test.jpg'
output = "out.jpg"

cv2.imwrite(output, remove_glare.remove_glare(fundus.extract_fundus(filename)))
print theia.grade_request(open(output))
