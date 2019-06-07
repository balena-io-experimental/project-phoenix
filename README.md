
https://wiki.freedesktop.org/www/Software/systemd/dbus/ 

#restart NetworkManager:

```
import dbus
sysbus = dbus.SystemBus()
systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')

machined1 = sysbus.get_object('org.freedesktop.machine1', '/org/freedesktop/machine1')
machine = dbus.Interface(machined1, 'org.freedesktop.machine1.Manager')

os-release = machine.GetMachineOSRelease('.host')
job = manager.RestartUnit('NetworkManager.service', 'fail')
```