# !/bin/bash
# This file installs necessary dependencies on rPI

# Start by checking python version
echo $(python -V)

# Then upgrade and update apt-get
echo "Updating and upgrading repositories..."
sudo apt-get update
sudo apt-get upgrade

# Upgrade rPI
echo "Updating rpi..."
sudo rpi-update

# Check if pip is installed
if command -v pip >/dev/null; then
	echo "pip is installed"
	echo $(pip -V)
else
	echo "pip is not installed, installing..."
	sudo apt-get install pip
fi

# Check python modules are installed: Checking using pip list | grep -F package-name
echo "Checking python modules..."
## 		pigpio
## 		picamera
## 		flask
## 		numpy
## 		cv2

## TODO: This can probably be implemented using a for loop or some better way...

# Start with cv2
if pip list | grep -F cv2 >/dev/null; then
	echo "cv2 is installed"
else
	echo "cv2 not installed, please install by following the instructions on http://www.pyimagesearch.com/2015/02/23/install-opencv-and-python-on-your-raspberry-pi-2-and-b/"
fi

# pigpio
if pip list | grep -F pigpio >/dev/null; then
	echo "pigpio is installed"
else
	echo "pigpio not installed, installing..."
	pip install pigpio
fi

# picamera
if pip list | grep -F picamera >/dev/null; then
	echo "picamera is installed"
else
	echo "picamera not installed, installing..."
	pip install picamera
fi

# flask
if pip list | grep -F flask >/dev/null; then
	echo "flask is installed"
else
	echo "flask not installed, installing..."
	pip install flask
fi

# numpy
if pip list | grep -F numpy >/dev/null; then
	echo "numpy is installed"
else
	echo "numpy not installed, installing..."
	pip install numpy
fi
