import dbus

class BalenaOS:
    class __BalenaOS:
        def __init__(self, arg):
            self.val = arg
        def __str__(self):
            return repr(self) + self.val
    instance = None
    try:
        #Define system bus
        sysbus = dbus.SystemBus()
        #Setup dbus for systemd
        systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
        #Setup dbus for machined
        machined1 = sysbus.get_object('org.freedesktop.machine1', '/org/freedesktop/machine1')
        machine = dbus.Interface(machined1, 'org.freedesktop.machine1.Manager')
    except:
        print("Cannot connect to OS system dbus")
        raise Exception('Cannot connect to OS system dbus, have you set the correct path? https://www.balena.io/docs/learn/develop/runtime/#dbus-communication-with-host-os')
   
    def __init__(self, arg):
        if not BalenaOS.instance:
            BalenaOS.instance = BalenaOS.__BalenaOS(arg)
        else:
            BalenaOS.instance.val = arg
        
        sysbus = dbus.SystemBus()
        systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __get_host_etc_os_release(self):
        return self.machine.GetMachineOSRelease('.host')

    def get_os_version(self):
        etcOsRelease = self.__get_host_etc_os_release()
        return str(etcOsRelease.get('VERSION'))

    def get_device_type(self):
        etcOsRelease = self.__get_host_etc_os_release()
        return str(etcOsRelease.get('MACHINE'))

    def get_os_pretty_name(self):
        etcOsRelease = self.__get_host_etc_os_release()
        return str(etcOsRelease.get('PRETTY_NAME'))
    
    def get_os_variant(self):
        etcOsRelease = self.__get_host_etc_os_release()
        return str(etcOsRelease.get('VARIANT'))

    def restart_service(self, serviceName):
        return self.manager.RestartUnit(serviceName, 'fail')

    def restart_modem_manager(self):
        self.restart_service('ModemManager.service')
    
    def restart_network_manager(self):
        self.restart_service('NetworkManager.service')

if __name__ == '__main__':
    os = BalenaOS('balenaOS dbus interface')
    print(os)