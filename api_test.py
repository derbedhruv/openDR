# Testing API on theia.media.mit.edu
# Author: Dhruv Joshi
# Using python since it's easier to put on the rPI
import requests		# pip install requests if you don't have it 
import json

# Get the key from external file
keyfile = open('key')
key = keyfile.readline()

## BEGIN THE REQUEST:
uri = 'https://theia.media.mit.edu/api/v1/uploadImage?key=' + key

response = requests.post(uri, files={'file': open('fundus.jpg', 'rb')})

if (response.status_code == 200):
    print "response OK"
    # convert response.text to json and parse as dictionary
    data = json.loads(response.text)
    grade = float(str(data['grade'])[1:-1])
    print "grade : " + str(grade)
else:
 	print "error."