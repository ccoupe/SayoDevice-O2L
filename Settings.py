import json

class Settings:

  def __init__(self, fn):
	self.load_settings(fn)
    
  def load_settings(self, fn):
    conf = json.load(open(fn))
    self.mqtt_server_ip = conf.get("mqtt_server_ip", "192.168.1.7")
    self.mqtt_port = conf.get("mqtt_port", 1883)
    self.homie_device = conf.get('homie_device', 'nopi_sayo')
    self.mqtt_client_name = conf.get("mqtt_client_name", self.homie_device)
    self.sayopath = None
    self.sayodev = None

    self.sayodev = conf.get("name", "SayoDevice SayoDevice O2L")
    self.topic = conf.get("topic", f"homie/{self.homie_device}/button/set")
    self.left = conf.get('left','start')
    self.right = conf.get('right', 'halt')
