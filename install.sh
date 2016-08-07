# !/bin/bash
# This file installs necessary dependencies on rPI

# Start by checking python version
echo $(python -V)

## TODO: Check PYTHONPATH and other environment variables

# Then upgrade and update apt-get
echo "Updating and upgrading repositories (Will require permissions)..."
sudo apt-get -y update
sudo apt-get -y upgrade

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

## TODO: Enable camera without needing to do raspi-config

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
	# Modified version of the install-opencv.sh script made by Manuel Ignacio Lopez Quintero (github user milq)
	# Made to suit raspberry pi and the work we would be doing
	### INSTALLING DEPENDENCIES
	## TODO: Trim these further
	
	# Build tools:
	sudo apt-get install -y build-essential cmake
	
	# GUI 
	sudo apt-get install -y qt5-default libvtk6-dev
	
	# Media I/O:
	sudo apt-get install -y zlib1g-dev libjpeg-dev libwebp-dev libpng-dev libtiff5-dev libjasper-dev libopenexr-dev libgdal-dev
	
	# Video I/O:
	sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev yasm libopencore-amrnb-dev libopencore-amrwb-dev libv4l-dev libxine2-dev
	
	# Parallelism and linear algebra libraries:
	sudo apt-get install -y libtbb-dev libeigen3-dev
	
	# Python:
	sudo apt-get install -y python-dev python-tk python-numpy python3-dev python3-tk python3-numpy
	
	# Java:
	sudo apt-get install -y ant default-jdk
	
	# Documentation:
	sudo apt-get install -y doxygen

	# We fetch OpenCV 2.4.8 which we're using and testing on
	sudo apt-get install -y unzip wget
	wget https://github.com/Itseez/opencv/archive/2.4.8.zip
	unzip 2.4.8.zip
	rm 2.4.8.zip
	mv opencv-2.4.8 OpenCV
	cd OpenCV
	mkdir build
	cd build

	# Important: We would run a custom CMAKE command to only make things we need
	# This drastically cuts down install time
	cmake -DBUILD_EXAMPLES=ON -DBUILD_JPEG=ON -DBUILD_opencv_calib3d=OFF -DBUILD_opencv_gpu=OFF -DBUILD_opencv_highgui=OFF -DBUILD_opencv_java=OFF -DBUILD_opencv_ts=OFF -DBUILD_opencv_video=OFF -DBUILD_opencv_videostab=OFF -DWITH_1394=OFF -DWITH_CUDA=OFF -DWITH_FFMPEG=OFF -DWITH_GIGEAPI=OFF -DWITH_GSTREAMER=OFF -DWITH_LIBV4L=OFF -DWITH_TIFF=OFF -DWITH_V4L=OFF ..
	
	# Then we make withonly one core to avoid issues...
	echo "Building opencv - this will take some time!"
	make
	sudo make install
	sudo ldconfig

	## TODO: Is apt-get install python-opencv enough for our requirements? Is that easier?
	echo "Finished installing OpenCV..now will setup the system to run OWL.."
	
fi

## TODO: Add installer and builder for extra functions!

# For installing flask setting for pi so that the server starts on boot
## TODO: Move all this to cronjob on boot
## TODO: All the server logs should be appended into a file
echo "Setting up OWL server to run on boot..."
# We first need to setup the pigpiod deamon to run on boot
(sudo crontab -l; echo "@reboot sudo pigpiod")|sudo crontab -
(crontab -l; echo "@reboot python /home/pi/openDR/fundus.py >> /home/pi/openDR/flask.log 2>&1")|crontab -


# Installing chromium browser - required for kiosk mode
echo "Installing chromium browser..."
wget -qO - http://bintray.com/user/downloadSubjectPublicKey?username=bintray | sudo apt-key add -
echo "deb http://dl.bintray.com/kusti8/chromium-rpi jessie main" | sudo tee -a /etc/apt/sources.list
sudo apt-get install -y chromium-browser


# Setting up kiosk mode - fullscreen app on boot
echo "Setting up Kiosk mode"
cat <<EOT >> ~/.config/lxsession/LXDE-pi/autostart
@xset s off
@xset -dpms
@xsetsnoblank

@sed­ -i's/"exited_cleanly":false/"exited_cleanly": true/'~/.config/chromium/Default/Preferences
@chromium­-browser --­­noerrdialogs --­­kiosk 127.0.0.1:8000 --incognito

EOT

## TODO: Install drivers for the touch screen display

# Finally should reboot the pi
# sudo reboot
