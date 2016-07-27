## Open Indirect Opthalmoscope (OIO)
_Authors: Ayush Yadav, Ebin Philip, Dhruv Joshi_

_Acknowledgements: Tristan Swedish, Devesh Jain_

Built at the Srujana Center for Innovation, LV Prasad Eye Institute, Hyderabad, India

OIO (or **"OWL"**, because OIO looks like one) is an ultra low-cost, open hardware device to image the retina (also called imaging the [fundus of the eye](https://en.wikipedia.org/wiki/Fundus_(eye))). Having the ability to image the retina easily and with low cost is invaluable in the early detection of potentially vision-threatening diseases, such as [diabetic retinopathy](https://en.wikipedia.org/wiki/Diabetic_retinopathy).

Read more about our device at our [website](http://lvpmitra.com/oio#introduction).

## LICENSE AND DISCLAIMER
This software is covered by the MIT License (see license.txt). 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Software Versions used
* OpenCV (cv2) 2.4.9.1
* Python 2.7.11+
* GCC 5.3.2

## Hardware platform
Details about assembly and parts is given on our [hackaday page](https://hackaday.io/project/11943-open-indirect-ophthalmoscope). Our software is designed and tested on a raspberry PI v2B and 3B, with M12 mount rPI cameras (through DSI cable).

## Dependencies
All dependencies can be installed by running `install.sh`

## How to run
Simply run `run.sh`

## Under the hood


=======
The GUI is run as a fullscreen webapp served with Flask. Our system's backbone is Python.
The folder structure is as follows (All individual folders have their own readme):


openDR  
   |---experimental_modules  
   |---images  
   |---static  
   |---templates  


* `experimental_modules` contains work in progress python modules. 
* `images` contains the images taken using the device. Images are stored in a folder named with the MR Number, and image names are of the format `MR_no_i_j.jpg` where i and j are integers. _i_ indicates session no and _j_ indicates pic number within that session.
* `static` contains all static elements (css, fonts, images, javascript) for the webapp gui which is served.
* `templates` contains all html for the webapp

The main functionality is written in `openDR/fundus_mod3.py`. This code polls for a button press and captures two images in quick succession (illuminating by two separate LEDs controlled by GPIO). The images are processed and then saved.

======= For Deploying application======

The repository must be cloned into the 'home' folder of Raspberry Pi, i.e., "/home/pi/" or just the '~' path. 
The name of the user should be 'pi'


The folder structure of deployable application is as follows:

- openDR #Main Folder

	- images #Folder
		
		Used for storing all clicked images and vids
	
	- static #Folder
		
		Used for storing all the static files for flask app like CSS, images etc. 
		
		Also has the JQ Keyboard Module
		
		-fonts  #Folder
		
		-css    #Folder
		
		-images #Folder
		
		-js     #Folder
	
	- templates #Folder
		
		Storing all the webpages of the HTML
	
	- name #File
		
		Stores the image number of the image last clicked and stores on the device
	
	- .gitignore #File

	- Fundus_cam.py #File
		
		Stores class which allows for the creation of object controlling the Picamer
		
		The various functions of the camera are controlled via this file's class
		
		It is imported into the fundus_mod3.py to make it work

	- fundus_mod3.py #File
		
		Various iterations of code have resulted in such naming of the file
		
		It is the integrative module which integrates the device, GUI and camera
		
		It has the flask server which is loaded on startup of device
		
		Any integrations are to be done from this file unless a major upgrade is being pushed


	- simplehttp.sh
		
		It creates a python simplehttp server on port 8000 to allow for transfer of files from the device
		
		It's a temporary hack and a better method would be employed for it soon enough

	- license.txt
		
		File with the MIT LICENSE

	- README.md
		
		Primary instruction and information manuel 
