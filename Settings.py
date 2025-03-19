import json
from evdev import InputDevice, categorize, ecodes , list_devices
class Settings:

  def __init__(self, fn, log):
    self.load_settings(fn)
    self.log = log
    
  def load_settings(self, fn):
    conf = json.load(open(fn))
    self.hmqtt = None	# mqtt.client handle set up after load
    self.mqtt_server_ip = conf.get("mqtt_server_ip", "192.168.1.7")
    self.mqtt_port = conf.get("mqtt_port", 1883)
    self.homie_device = conf.get('homie_device', 'nopi_sayo')
    self.mqtt_client_name = conf.get("mqtt_client_name", self.homie_device)
    self.sayopath = None
    self.keydev = None
    self.sayodev = conf.get("name", "SayoDevice SayoDevice O2L")
    self.idVendor = conf.get("idVendor", "8089").upper()
    self.idProduct = conf.get("idProduct", "000c").upper()
    self.topic = conf.get("topic", f"homie/{self.homie_device}/button/set")
    self.left = conf.get('left','start')
    self.right = conf.get('right', 'halt') 
    '''
    devices = [InputDevice(path) for path in list_devices()]
    print("From", devices)
    for device in devices:
      if device.name.startswith(self.sayodev):
        print("Found one")
        self.sayopath = device.path
        break
      print(device.path, device.name, device.phys)
    if self.sayopath:
      self.keydev = InputDevice(self.sayopath)
    else:
      print("Failed to find a SayoDevice")
    '''
