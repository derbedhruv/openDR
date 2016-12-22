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
Details about assembly and parts is given on our [hackaday page](https://hackaday.io/project/11943-open-indirect-ophthalmoscope). Our software is designed and tested on a raspberry PI v2B and 3B, with M12 mount rPI cameras (through DSI cable). The OS on the raspberry PI we use is [Wheezy](https://downloads.raspberrypi.org/raspbian/images/2013-07-26-wheezy-raspbian/).

## Dependencies
All dependencies can be installed by running `install.sh`, sudo password would be required if some dependencies are not present. We recommend installing the software on a fresh dedicated rPI.

## Deploying the application
The repository must be cloned into the 'home' folder of Raspberry Pi, i.e., `/home/pi/` or just the `~` path, all environment variables are set with respect to this!
The name of the user should be **pi** (which is the default on new rPI OS installations).


## Under the hood

The GUI is run as a fullscreen webapp served with Flask. Our system's backbone is Python.
The folder structure is as follows (All individual folders have their own readme):

####Folder Structure
openDR  
   |---experimental_modules  
   |---images  
   |---static  
   |---templates  


`experimental_modules` contains work in progress python modules. 

`images` contains the images taken using the device. Images are stored in a folder named with the MR Number, and image names are of the format `MR_no_i_j.jpg` where i and j are integers. _i_ indicates session no and _j_ indicates pic number within that session.

`static` contains all static elements (css, fonts, images, javascript) for the webapp gui which is served.

`templates` contains all html for the webapp

#### Important Files
`fundus_mod3.py` has the main functionality, and integrates the GUI and imaging. This code polls for a button press and captures two images in quick succession (illuminating by two separate LEDs controlled by GPIO). The images are processed and then saved.

`name` stores the image number of the image last clicked and stores on the device (temporary hack!)

`Fundus_cam.py` stores the class which allows for the creation of object controlling the Picamera. 

`simplehttp.sh` creates a python simplehttp server on port 8000 to allow for transfer of files from the device.
