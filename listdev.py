import evdev
from evdev import InputDevice, categorize, ecodes 

sayodev = None
dev = None
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
print("From", devices)
for device in devices:
    print(device.path, device.name, device.phys)
    if device.name.startswith("SayoDevice SayoDevice O2L"):
        print("A hit!")
        sayodev = device.path
        break
if sayodev:
  dev = InputDevice(sayodev)
  #print("Have", dev.leds(verbose=True)) #empty
  #print("active_keys", dev.active_keys(verbose=True)) #empty
  #print(device.capabilities(verbose=True))
else:
  print("Not Found!!!")
print("Begin loop, Ctrl-C to exit")
for event in dev.read_loop():
  if event.type == ecodes.EV_KEY:
    if event.code == 44 and event.value == 1: # 1 is key down
      print('left key')
    if event.code == 45 and event.value == 1:
      print('right key')
    
