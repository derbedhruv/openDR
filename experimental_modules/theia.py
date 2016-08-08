# API calls on theia.media.mit.edu in a handy module
# Author: Dhruv Joshi
# Using python since it's easier to put on the rPI
import requests		# pip install requests if you don't have it 
import json

# Get the key from external file
keyfile = open('key')
key = keyfile.readline()

def grade_request(file):
    # makes the request to the theia interface and returns the grade of that image.
	# if there is something wrong, it returns -1
	# argument - file object
	uri = 'https://theia.media.mit.edu/api/v1/uploadImage?key=' + key
	response = requests.post(uri, files={'file': file})
	
	if (response.status_code == 200):
		# print "response OK"
		# convert response.text to json and parse as dictionary
		data = json.loads(response.text)
		grade = float(str(data['grade'])[1:-1])
		return grade
	else:
		return -1

## BEGIN THE REQUEST:
# print grade_request(open('normal1.jpg', 'rb'))