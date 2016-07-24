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
<<<<<<< HEAD
The folder structure is as follows:

- openDR #Main Folder

	- images #Folder
		USED FOR STORING ALL CLICKED IMAGES AND VIDS
	
	- static #Folder
		USED FOR KEEPING ALL THE STATIC FILES FOR FLASK LIKE CSS, IMAGES ETC
		ALSO HOLDS THE JQ KEYBOARD MODULE
		-fonts  #Folder
		-css    #Folder
		-images #Folder
		-js     #Folder
	
	- templates #Folder
		KEEPS ALL THE WEBPAGES AS THEIR HTMLS
	
	- name #File
		STORES THE IMAGE NUMBER OF THE IMAGE LAST CLICKED AND STORES ON DEVICE
	
	- .gitignore #File

	- Fundus_cam.py #File
		STORES CLASS WHICH ALLOWS FOR THE CREATION OF OBJECT CONROLLING THE PICAMERA
		THE VARIOUS FUNCTIONS OF THE CAMERA ARE CONTROLLED VIA THIS FILE'S CLASS
		IT IS IMPORTED INTO THE fundus_mod3.py TO MAKE IT WORK

	- fundus_mod3.py #File
		VARIOUS ITERATIONS HAVE LED TO SUCH A WEIRD NAME FOR THE FILE
		IT IS THE INTEGRATIVE MODULE WHICH INTEGRATES THE DEVICE, GUI AND CAMERA
		IT HAS THE FLASK SERVER WHICH IS LOADED ON STARTUP OF DEVICE
		ANY INTEGRATIONS ARE TO BE DONE FROM THIS FILE ITSELF UNLESS A MAJOR UPGRADE IS BEING PUSHED


	- simplehttp.sh
		IT CREATES A PYTHON SIMPLEHTTP SERVER ON PORT 8000 TO ALLOW FOR TRANSFER OF FILES FROM THE DEVICE
		IT'S A TEMPORARY HACK AND A BETTER METHOD WOULD BE EMPLOYED FOR IT SOON ENOUGH

	- license.txt
		FILE HAVING THE MIT LICENSE

	- README.md
		FILE WITH ALL INSTRUCTIONS
=======
The GUI is run as a fullscreen webapp served with Flask. Our system's backbone is Python.
The folder structure is as follows (All individual folders have their own readme):

```
openDR  
   |---experimental_modules  
   |---images  
   |---static  
   |---templates  
```
* `experimental_modules` contains work in progress python modules. 
* `images` contains the images taken using the device. Images are stored in a folder named with the MR Number, and image names are of the format `MR_no_i_j.jpg` where i and j are integers. _i_ indicates session no and _j_ indicates pic number within that session.
* `static` contains all static elements (css, fonts, images, javascript) for the webapp gui which is served.
* `templates` contains all html for the webapp

The main functionality is written in `openDR/fundus_mod3.py`. This code polls for a button press and captures two images in quick succession (illuminating by two separate LEDs controlled by GPIO). The images are processed and then saved.
>>>>>>> 78aacd4da695b33b011c6b5f3eba7858cf5b3dda
