import dbus

import gi

gi.require_version('NM', '1.0')
gi.require_version('GLib', '2.0')
gi.require_version('ModemManager', '1.0')

from gi.repository import NM, GLib
from gi.repository import Gio, ModemManager

class BalenaOS:
    class __BalenaOS:
        def __init__(self, arg):
            """Initialize a balenaOS singleton"""
            self.val = arg
            #Define system bus
            self.sysbus = dbus.SystemBus()
            #Setup dbus for systemd
            self.systemd1 = self.sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
            self.manager = dbus.Interface(self.systemd1, 'org.freedesktop.systemd1.Manager')
            #Setup dbus for machined
            self.machined1 = self.sysbus.get_object('org.freedesktop.machine1', '/org/freedesktop/machine1')
            self.machine = dbus.Interface(self.machined1, 'org.freedesktop.machine1.Manager')
        def __str__(self):
            return repr(self) + self.val
    instance = None

    def __init__(self, arg):
        if not BalenaOS.instance:
            BalenaOS.instance = BalenaOS.__BalenaOS(arg)
        else:
            BalenaOS.instance.val = arg

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __get_host_etc_os_release(self):
        """Read the hostOS /etc/os-release"""
        return self.machine.GetMachineOSRelease('.host')

    def get_os_version(self):
        """Return the hostOS version string"""
        etcOsRelease = self.__get_host_etc_os_release()
        return str(etcOsRelease.get('VERSION'))

    def get_os_pretty_name(self):
        """Return the hostOS version string"""
        etcOsRelease = self.__get_host_etc_os_release()
        return str(etcOsRelease.get('PRETTY_NAME'))

    def get_device_type(self):
        """Return the Balena Device Type string"""
        etcOsRelease = self.__get_host_etc_os_release()
        return str(etcOsRelease.get('MACHINE'))
    
    def get_os_variant(self):
        """Return the hostOS variant type"""
        etcOsRelease = self.__get_host_etc_os_release()
        return str(etcOsRelease.get('VARIANT'))

    def print_os_info(self):
        """Print basic OS info"""
        print("Device: ", self.get_device_type())
        print("OS Version: ", self.get_os_version())
        print("OS Variant: ", self.get_os_variant())

    def restart_service(self, serviceName):
        """Restart a systemd service in the hostOS"""
        return self.manager.RestartUnit(serviceName, 'fail')

    def restart_modem_manager(self):
        """Restart the hostOS ModemManager"""
        self.restart_service('ModemManager.service')
    
    def restart_network_manager(self):
        """Restart hostOS NetworkManager service"""
        self.restart_service('NetworkManager.service')

class OsNetwork:
    instance = None
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if OsNetwork.instance == None:
            OsNetwork('')
        return OsNetwork.instance

    class __OsNetwork:
        def __init__(self, arg):
            self.val = arg
            self.client = NM.Client.new(None)
            modem_connection = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
            self.modem_manager = ModemManager.Manager.new_sync(modem_connection, Gio.DBusObjectManagerClientFlags.DO_NOT_AUTO_START, None)
            #TODO: improve how we get primary modem
            modem = None
            for obj in self.modem_manager.get_objects():
                modem = obj.get_modem()
            self.object_added_id = self.modem_manager.connect('object-added', on_modem_added)
            self.modem = modem

        def __str__(self):
            return repr(self) + self.val    

    def __init__(self, arg):
        if not OsNetwork.instance:
            OsNetwork.instance = OsNetwork.__OsNetwork(arg)
        else:
            OsNetwork.instance.val = arg

    def __getattr__(self, name):
        return getattr(self.instance, name)
    
    def get_connectivity_state(self):
        """Get NetworkManager Connectivity State"""
        state = self.client.get_state()
        return self.__get_nm_state_string(str(int(state)))

    def __get_nm_state_string(self, state):
        """Map integers to NM state strings"""
        return {
            '70': 'CONNECTED_GLOBAL',
            '60': 'CONNECTED_SITE',
            '50': 'CONNECTED_LOCAL',
            '40': 'CONNECTING',
            '30': 'DISCONNECTING',
            '20': 'DISCONNECTED',
            '10': 'ASLEEP',
            '0' : 'UNKNOWN',
        }.get(state, 'UNKNOWN')
    
    def __get_connectivity_state_string(self, state):
        """Map integers to connectivity state strings"""
        return {
            '0': 'UNKNOWN',
            '1': 'NONE',
            '2': 'PORTAL',
            '3': 'LIMITED',
            '4': 'FULL',
        }.get(state, 'UNKNOWN')

    def connectivity_changed(self, instance, param):
        """Call back on connectivity state change"""
        #TODO: move this of out class
        connectivity = int(instance.get_property(param.name))
        print('[Notify] Connectivity Changed: ', self.__get_connectivity_state_string(str(connectivity)))
        #TODO: build logic to restart NM or MM to ensure connectivity.

    def primary_connection_changed(self, instance, param):
        """Call back for when primary connection changes"""
        primary_connection = instance.get_property(param.name)
        self.print_addresses(primary_connection)

    def print_addresses(self, active_connection):
        """Print IPv4 Address of a connection"""
        if active_connection:
            ip4_config = active_connection.get_ip4_config()
            addrs = ip4_config.get_addresses()

            for addr in addrs:
                addr = addr.get_address()
                print("Primary IP address: ", addr)
        else:
            print("No active connection")

    def send_modem_at_command(self, command):
        """Send AT command to the modem"""
        return self.modem.command_sync(command, 10, None)

    def print_modem_info(self):
        """Print out basic modem info"""
        if self.modem:
            print("Modem Manufacturer: ", self.modem.get_manufacturer())
            print("Modem Signal: ", self.modem.get_signal_quality())
            print("Modem Model: ", self.modem.get_model())
        else:
            print("No modem available")

# Util functions
def on_modem_added(manager, obj):
    """Updates OsNetwork.modem instance when Modem is detected"""
    net = OsNetwork.getInstance()
    modem = None
    for obj in manager.get_objects():
        modem = obj.get_modem()
    net.modem = modem

    print('[Notify] %s (%s) modem managed by ModemManager [%s]: %s' %
            (modem.get_manufacturer(),
            modem.get_model(),
            modem.get_equipment_identifier(),
            obj.get_object_path()))

if __name__ == '__main__':
    os = BalenaOS('balenaOS dbus interface')
    print(os)