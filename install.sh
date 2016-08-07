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
sudo pip install --upgrade picamera[array]

# flask
echo "Checking Flask..."
sudo pip install --upgrade flask

# numpy
echo "Checking numpy..."
sudo pip install --upgrade numpy

# Start with cv2
if python -c "import cv2" >/dev/null; then
	echo "openCV is installed"
	## TODO: Check version
	# If it is not proper, then sudo apt-get autoremove libopencv-dev python-opencv
else
	echo "OpenCV not installed, will proceed to install automatically. This will take upto 4 hours!"
	# Download the installer from Manuel's website
	echo "Fetching installer: built by Manuel Ignacio Lopez Quintero - thanks a lot!"
	wget https://raw.githubusercontent.com/milq/scripts-ubuntu-debian/master/install-opencv.sh
	bash install-opencv.sh
fi

## TODO: Add installer and builder for extra functions!

# For installing flask setting for pi so that the server starts on boot
## TODO: Move all this to cronjob on boot
## TODO: All the server logs should be appended into a file
echo "Setting up OWL server to run on boot..."
(crontab -l; echo "@reboot python /home/pi/openDR/fundus.py >> /home/pi/openDR/flask.log 2>&1")|crontab -



# Installing chromium browser - required for kiosk mode
wget -qO - http://bintray.com/user/downloadSubjectPublicKey?username=bintray | sudo apt-key add -
echo "deb http://dl.bintray.com/kusti8/chromium-rpi jessie main" | sudo tee -a /etc/apt/sources.list
sudo apt-get update
sudo apt-get install chromium-browser


# Setting up kiosk mode - fullscreen app on boot
echo "Setting up Kiosk mode"
cat <<EOT >> ~/.config/lxsession/LXDE-pi/autostart
@xset s off
@xset -dpms
@xsetsnoblank

@sed­ -i's/"exited_cleanly":false/"exited_cleanly": true/'~/.config/chromium/Default/Preferences
@chromium­-browser --­­noerrdialogs --­­kiosk 127.0.0.1:8000 --incognito

EOT
