
Installation
============

1 - Install the driver from the folder USB8RelayManager
    CDM20802_Setup.exe
    if possible in admin right

2 - Launch the software USB 8 RElay Manager v1.4.exe to verify the good connection with the hardware
    - connect the card
    - on manual tab click on the first one to check if the sate of the relay change

3 - Install the USB filter from the libusb folder
    - choose your good version 32 or 64 bits (not tested on 32b)
    - install the libusb filter-win.exe
    - click install filter
    - select the one with pid= and vid= 
    - then ok

    the filter allows to access from the computer without launching the relay Manager


folder
=====
swith_ui.py is the python software
    require
    -------
        - python 3.7 or higer
        - pyqt5         pip install PyQt5
        - pyusb         pip install pyusb  

switch_ui.exe is the binary source of Switch.py 

settings.txt
    allow to change the pid and vid if a new card is provide or another type of USB

pictures ==> folder
    - contains the pictures for the Switch software

init.py
    - allow Switch to be a module in another application

relay.py
    - allow to play with on and off the Switch
    
    usage 
    -----

    initialise card
    select card
    swith on and off relais
    at closing of script or software => off relais ==> should be instruced in the script

example:
========

import relay
VID = 0x0403                   
PID = 0x6001  
rb = relay.FT245R(VID, PID)         # open the instance for connecting the card(s)
dev = self.rb.list_dev()[0]         # allow to get a list of the card(s) and select the first one
rb.connect(dev)                     # connect the dev card

rb.switchoff(1)                     # off on relais 1
rb.switchon(1)                      # on on relais 1


### end of the script
for i in range(4):                  # up to 4 relais are possible but only one is used in our case
    rb.switchoff(i+1)               # starting from 1 and not 0
rb.disconnect()                     # disconnect the card to allow a new accessnext time