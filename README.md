The SayoDevice is a two button usb keypad. Linux sees it as a keyboard device. This a program that captures the keydowns and publishs them to and mqtt topic. This might be useful for Home Assistant or similar hubs like Hubitat.

There is a json file for configuration with entries for the mqtt broker ip addrees, port number, user name and password (if used on the mqtt brocker) and the the topic and payload for each key (left and right).

Likely to have permission problems on many Linux. 
`sudo setfacl -m u:ccoupe:rw /dev/input/event15` Of course, you have to change the user name and the event has to match what you have.
