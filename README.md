# Wedding Booth

1. Enable Camera module

Enable and Configure the camera module: https://www.raspberrypi.org/documentation/usage/camera/

2. Install Libraries

* Install Python 3.7+ :  https://www.raspberrypi.org/documentation/linux/software/python.md

* Install PyQt5 (runs the GUI): https://pypi.org/project/PyQt5/

* Install Picamera (library for the camera module of Raspberry pi): https://www.raspberrypi.org/documentation/linux/software/python.md

* Install Python module RPI.GPIO (library for control Raspberry GPIO for the arcade button): https://learn.adafruit.com/playing-sounds-and-using-buttons-with-raspberry-pi/install-python-module-rpi-dot-gpio

* Install PIL (Python Image Library): https://pillow.readthedocs.io/en/stable/

* Run the following commands to install onscreen keyboard for PyQt5 (h/t eyllanesc https://stackoverflow.com/questions/63719347/install-qtvirtualkeyboard-in-raspberry-pi):

    sudo apt-get update
    sudo apt install git build-essential
    sudo apt-get install python3-pyqt5 qt5-default qtdeclarative5-dev libqt5svg5-dev qtbase5-private-dev qml-module-qtquick-controls2 qml-module-qtquick-controls qml-module-qt-labs-folderlistmodel
    sudo apt-get install '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev
    git clone -b 5.11 https://github.com/qt/qtvirtualkeyboard.git
    cd qtvirtualkeyboard
    qmake 
    sudo make
    sudo make install

3. Using the App
To run the app, open a terminal, navigate to this folder, and type: python3 weddingbooth.py

If you want to test it without a button wire on GPIO Pin 25 of the pi, you can push down arrow of your keyboard.

Finally, I wanted to run the program at startup of the raspberry pi so I followed this tuto https://www.simplified.guide/linux/automatically-run-program-on-startup

The script which launch at startup is on the Github: photobooth-script.sh 


