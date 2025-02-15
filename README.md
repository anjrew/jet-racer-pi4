# Jetson Racer Pi4 - Ubuntu Noble 24.04 - ROS2 Jazzy

This repo contains code and instructions on how to get the Jetson Racer car from Waveshare running with a Raspberry Pi 4

## Setup instructions

1. Install Ubuntu for Raspberry Pi is available [here](https://ubuntu.com/download/raspberry-pi).
2. Once setup install through the debian packages for ROS by following these instructions [here](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html#id2)
3. [Setup the camera](https://www.youtube.com/watch?v=va7o7wzhEE4&ab_channel=gaseoustortoise)
4. Follow the guide here to make a vitual environment for the project [here](https://docs.python.org/3/library/venv.html) 
    a. `python3 -m venv venv`
5. Activate the virtual environment (and every time in the project) by running the following command
    a. `source venv/bin/activate`
6. Install Service of OLED Display
Use command belows to install service for OLED displaying. The OLED onboard can be used to display IP address, Voltage and current, etc.
```bash
cd ~
git clone https://github.com/anjrew/pi-display-ubuntu-server-24.04.git
cd pi-display
sudo ./install.sh
```

??? for picamera: https://github.com/raspberrypi/picamera2/issues/563#issuecomment-1981658308


## Other Resources
- [Jetracer DonkeyPi Repo](https://github.com/waveshare/donkeycar)
- [Jetracer DonkeyPi Wiki](https://www.waveshare.com/wiki/PiRacer_AI_Kit)
