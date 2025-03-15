from evdev import InputDevice, categorize, ecodes , list_devices
import paho.mqtt.client as mqtt
import json
import Settings
import sys
import argparse
import logging

hmqtt = None
settings = None

def mqtt_conn_init(st):
  global hmqtt
  hmqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, st.mqtt_client_name, False)
  hmqtt.connect(st.mqtt_server_ip, st.mqtt_port)
  
  hmqtt.publish(st.topic, None, qos=1,retain=False)
      
  # hmqtt.on_message = mqtt_message
  hmqtt.loop_start()
     
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
  
  settings = Settings.Settings(args["conf"])
  mqtt_conn_init(settings)
  
  for event in settings.keydev.read_loop():
    if event.type == ecodes.EV_KEY:
      if event.code == 44 and event.value == 1: # 1 is key down
        hmqtt.publish(settings.topic, settings.left, qos=1,retain=False)
        #print('left key')
      if event.code == 45 and event.value == 1:
        hmqtt.publish(settings.topic, settings.right, qos=1,retain=False)
        #print('right key')

if __name__ == '__main__':
  sys.exit(main())

