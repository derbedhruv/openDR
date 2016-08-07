# !/bin/bash
# This file installs necessary dependencies on rPI

# Start by checking python version
echo $(python -V)

## TODO: Check PYTHONPATH and other environment variables

# Then upgrade and update apt-get
echo "Updating and upgrading repositories (Will require permissions)..."
sudo apt-get update
sudo apt-get upgrade

# Upgrade rPI
echo "Updating rpi..."
sudo rpi-update

# Check if pip is installed
echo "Checking pip..."
sudo apt-get install python-pip

# Check python modules are installed: Checking using pip list | grep -F package-name
echo "Checking python modules..."
## 		pigpio
## 		picamera
## 		flask
## 		numpy
## 		cv2

# pigpio
if pip list | grep -F pigpio >/dev/null; then
	echo "pigpio is already installed"
else
	echo "pigpio not installed, installing ..."
	echo "Fetching latest version and unzipping..."
	wget abyz.co.uk/rpi/pigpio/pigpio.zip
	unzip pigpio.zip
	cd PIGPIO 
	make
	make install
fi

# picamera
echo "Checking picamera..."
sudo pip install --upgrade picamera

# flask
echo "Checking Flask..."
sudo pip install --upgrade flask

# numpy
echo "Checking numpy..."
sudo pip install --upgrade numpy

# Start with cv2
if pip list | grep -F cv2 >/dev/null; then
	echo "openCV is installed"
	## TODO: Check version
	# If it is not proper, then sudo apt-get autoremove libopencv-dev python-opencv
else
	echo "cv2 not installed, will proceed to install. This will take upto 4 hours!"
	# Download the installer from Manuel's website
	echo "Fetching installer: built by Manuel Ignacio Lopez Quintero - thanks a lot!"
	wget https://raw.githubusercontent.com/milq/scripts-ubuntu-debian/master/install-opencv.sh
	bash install-opencv.sh
fi

## TODO: Add installer and builder for extra functions!

#For installing flask setting for pi so that the server starts on boot

echo "export FLASK_APP=/home/pi/openDR/fundus_mod3.py" >> ~/.bashrc
echo "flask run" >> ~/.bashrc

#For installing chromium browser
wget -qO - http://bintray.com/user/downloadSubjectPublicKey?username=bintray | sudo apt-key add -
echo "deb http://dl.bintray.com/kusti8/chromium-rpi jessie main" | sudo tee -a /etc/apt/sources.list
sudo apt-get update
sudo apt-get install chromium-browser


#For running kiosk mode 

cat <<EOT >> ~/.config/lxsession/LXDE-pi/autostart
@xset s off
@xset -dpms
@xsetsnoblank

@sed­ -i's/"exited_cleanly":false/"exited_cleanly": true/'~/.config/chromium/Default/Preferences
@chromium­-browser --­­noerrdialogs --­­kiosk 127.0.0.1:8000 --incognito

EOT
