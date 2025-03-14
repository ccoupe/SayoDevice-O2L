import evdev

sayodev = None
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    if device.name.startswith("SayoDevice SayoDevice O2L"):
        print("A hit!")
        sayodev = device.path
        break
    print(device.path, device.name, device.phys)
if sayodev:
  dev = evdev.InputDevice(sayodev)
  print("Have", dev.leds(verbose=True))
  print("active_keys", dev.active_keys(verbose=True))
  print(device.capabilities(verbose=True))
else:
  print("Not Found!!!")
