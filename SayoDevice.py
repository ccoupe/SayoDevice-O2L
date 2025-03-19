import pyudev
from threading import Lock, Thread
import re
from evdev import InputDevice, categorize, ecodes , list_devices

class SayoDevice:

  def __init__(self, settings):
    self.st = settings
    self.watching = {}
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='input')
    observer = pyudev.MonitorObserver(monitor, self.monitor_device_event, name='monitor-observer')
    observer.daemon
    observer.start()
    

  def monitor_device_event(self, action, device):
    #print('background event {0}: {1}'.format(action, device))
    #print(device.get('ID_VENDOR', 'NADA')) # retirms 'SayoDevice'
    # begin hack because I don't understand how to get the attribute keys
    devs = str(device)
    flds = devs.split('/')
    ev = flds[-1]
    r = re.search('[0-9]+',ev)
    if r: ev = 'event'+r.group()
    else: return
    ids = flds[-4]
    r = re.search(':[0-9A-F]+:[0-9A-F]+', ids)
    if r: ids = r.group()
    else: return
    #print(ids[1:5],self.st.idVendor,'and',ids[6:10],self.st.idProduct)
    
    log = self.st.log
    if ids[1:5]==self.st.idVendor and ids[6:10]==self.st.idProduct:
      if action == 'add':
        path = "/dev/input/"+ev
        th = Thread(target=self.readkey, args=(path,))
        self.watching[devs] = th
        log.warn(f'added {path}')
        th.start()
      elif action == 'remove':
        if self.watching.get(devs, None):
          th = self.watching.get(devs, None)
          try:
            th._stop()
          except (OSError, AssertionError):
            log.warn("Exception caught in monitor_device_event()")
          self.watching[devs] = None
          log.warn(f'removed /dev/input/{ev}')
   
  def readkey(self, sayopath):
    settings = self.st
    hmqtt = settings.hmqtt
    log = settings.log
    
    log.warn(f'thread started for {sayopath}')
    keydev = InputDevice(sayopath)
    keydev.grab()
    try:
      for event in keydev.read_loop():
        if event.type == ecodes.EV_KEY:
          if event.code == 44 and event.value == 1: # 1 is key down
            hmqtt.publish(settings.topic, settings.left, qos=1,retain=False)
            #print('left key')
          if event.code == 45 and event.value == 1:
            hmqtt.publish(settings.topic, settings.right, qos=1,retain=False)
            #print('right key')
    except (OSError, AssertionError):
     log.warn("Exception caught in readkey()")

  def addExisting(self):
    settings = self.st
    devices = [InputDevice(path) for path in list_devices()]
    sayopath = None
    for device in devices:
      if device.name.startswith(settings.sayodev):
        sayopath = device.path
        break
    if sayopath:
      # remember that hack comment above. it gets worse. Cobble together
      # a string that the hack will use.
      evstr = str(device.path).split('/')[-1]
      hackstr = f"a/:{settings.idVendor}:{settings.idProduct}/1/2/{evstr}"
      settings.log.warn(f'simulate add {hackstr} for existing device')
      self.monitor_device_event('add', hackstr)
    else:
      pass # it's Ok to not find one
 
