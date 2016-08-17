# API calls on theia.media.mit.edu in a handy module
# Author: Dhruv Joshi
# Using python since it's easier to put on the rPI
import requests		# pip install requests if you don't have it 
import json

def grade_request(f):
    # makes the request to the theia interface and returns the grade of that image.
	# if there is something wrong, it returns -1
	# argument - file object
	# Get the key from external file
        try:
            keyfile = open('/home/pi/openDR/key')
            key = keyfile.readline()
        except IOError:
            print "CANNOT FIND KEY FOR THEIA. PLEASE CHECK."
            return -1

        image_file = open(f)
	uri = 'https://theia.media.mit.edu/api/v1/uploadImage?key=' + key
	response = requests.post(uri, files={'file': image_file})
	
	if (response.status_code == 200):
                # TODO: check for BAD API KEY
		# print "response OK"
		# convert response.text to json and parse as dictionary
		data = json.loads(response.text)
		grade = float(str(data['grade'])[1:-1])
		return grade
	else:
		return -1


## BEGIN THE REQUEST:
# print grade_request(open('normal1.jpg', 'rb'))
