from evdev import InputDevice, categorize, ecodes , list_devices
import paho.mqtt.client as mqtt
import json


sayopath = None
sayodev = None
devices = [InputDevice(path) for path in list_devices()]
for device in devices:
    if device.name.startswith("SayoDevice SayoDevice O2L"):
        print("A hit!")
        sayopath = device.path
        break
    print(device.path, device.name, device.phys)
if sayopath:
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
      
def main():
  global settings, hmqtt
  loglevels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
  ap = argparse.ArgumentParser()
  ap.add_argument("-c", "--conf", required=True, type=str,
    help="path and name of the json configuration file")
  ap.add_argument("-s", "--syslog", action = 'store_true',
    default=False, help="use syslog")
  args = vars(ap.parse_args())
  
  # logging setup
  log = logging.getLogger('sayodev')
  if args['syslog']:
    log.setLevel(logging.INFO)
    handler = logging.handlers.SysLogHandler(address = '/dev/log')
    # formatter for syslog (no date/time or appname.
    formatter = logging.Formatter('%(name)s-%(levelname)-5s: %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
  else:
    logging.basicConfig(level=logging.INFO,datefmt="%H:%M:%S",format='%(asctime)s %(levelname)-5s %(message)s')
  
  settings = Settings(args["conf"])
  verify(settings.
  mqtt_conn_init(settings)
	
if __name__ == '__main__':
  sys.exit(main())

