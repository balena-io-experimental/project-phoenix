import gi

gi.require_version('NM', '1.0')
gi.require_version('GLib', '2.0')
gi.require_version('ModemManager', '1.0')

from gi.repository import NM, GLib
from gi.repository import Gio, ModemManager

from balenaos import BalenaOS

def main():
    #Create balenaOS singleton
    os = BalenaOS('OS dbus interface')
    
    #create a NM client
    client = NM.Client.new(None)

    #create a MM modem instance
    modem_connection = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
    modem_manager = ModemManager.Manager.new_sync(modem_connection, Gio.DBusObjectManagerClientFlags.DO_NOT_AUTO_START, None)
    modem = get_current_modem(modem_manager)
    
    #Show device and OS info
    print_os_info(os)

    #Show the current modem info
    print_modem_info(modem)

    #listen for changes on the default connection
    client.connect('notify::primary-connection', primary_connection_changed)
    primary_connection = client.get_primary_connection()

    print_addresses(primary_connection)

    GLib.MainLoop().run()

def print_os_info(osInstance):
    print("Device: ", osInstance.get_device_type())
    print("OS Version: ", osInstance.get_os_version())
    print("OS Variant: ", osInstance.get_os_variant())

def get_current_modem(manager):
    modem = None
    for obj in manager.get_objects():
        modem = obj.get_modem()
    return modem

def print_modem_info(modem):
    print("Modem Manufacturer: ", modem.get_manufacturer())
    print("Modem Signal: ", modem.get_signal_quality())
    print("Modem Model: ", modem.get_model())

def primary_connection_changed(instance, param):
    primary_connection = instance.get_property(param.name)
    print_addresses(primary_connection)


def print_addresses(active_connection):
    ip4_config = active_connection.get_ip4_config()

    addrs = ip4_config.get_addresses()

    for addr in addrs:
        addr = addr.get_address()

        print("Primary IP address: ", addr)

main()