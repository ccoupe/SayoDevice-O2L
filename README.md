The SayoDevice is a two button usb keypad. Linux sees it as a keyboard device. 
This a program that captures the keydowns and publishs them to and mqtt topic. 
This might be useful for Home Assistant or similar hubs like Hubitat.

There is a json file for configuration with entries for the mqtt broker ip 
addrees, port number, user name and password (if used on the mqtt brocker) 
and the the topic and payload for each key (left and right).

Likely to have permission problems on many Linux. 
`sudo setfacl -m u:ccoupe:rw /dev/input/event15` Of course, you have to 
change the user name and the event has to match what you have.

`make install`

## Version 1
 (keyread.py) is a simple Python program that scans /dev/input/ for eventX
entries that match the name in the user supplied json file. It attempts
to isolate the key processing from the keypad to just this app via a call
to grab()

It is REQUIRED that you have permissions to open the device. The following
line will do that. Replace with your user name and the eventX of your device
`sudo setfacl -m u:ccoupe:rw /dev/input/event15`

Do this every time the device is inserted into the system - the permission
goes away when the device is removed or the system is rebooted. This is 
a PITA. It can be fixed by adding this file to
/etc/udev/rules.d/51-sayodevice.rules
`SUBSYSTEMS=="usb", ATTRS{idVendor}=="8089", ATTRS{idProduct}=="000c", GROUP="users", MODE="0666"
` Then do a a `sudo udevadm control --reload-rules`. Some say you have to
reboot to see the new rule take effect. Not true for me. 

Another race condition is that the keypad.py process needs to be running
from systemd (--user) but it can't be 

## Version 2 - keypadv2.py 
Is more sophisticated. It can detect the insertion and removal 
of the SayoDevice, attach to it and direct it. It could be written in C, Go 
or Python. Currently, Python. It is not a full device driver and is started
by systemd --user in /etc/xdg/systemd/user. This requires the 51-sayodevice.rules
file in /etc/udev/rules.d (or possibly /usr/lib/
