import gi

gi.require_version('GLib', '2.0')
# gi.require_version('ModemManager', '1.0')
# from gi.repository import Gio, ModemManager
from gi.repository import GLib
from balenaos import BalenaOS, OsNetwork

def main():
    #Create balenaOS singleton
    os = BalenaOS('OS dbus interface')
    net = OsNetwork('Network interface')

    #create a NM client
    client = net.client
    
    #Show device and OS info
    os.print_os_info()

    # #create a MM modem instance
    # modem_connection = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
    # modem_manager = ModemManager.Manager.new_sync(modem_connection, Gio.DBusObjectManagerClientFlags.DO_NOT_AUTO_START, None)
    # modem = get_current_modem(modem_manager)
    # #Show the current modem info
    # print_modem_info(modem)

    #listen for changes on the default connection
    client.connect('notify::primary-connection', net.primary_connection_changed)
    primary_connection = client.get_primary_connection()

    net.print_addresses(primary_connection)

    GLib.MainLoop().run()

# def get_current_modem(manager):
#     modem = None
#     for obj in manager.get_objects():
#         modem = obj.get_modem()
#     return modem

# def print_modem_info(modem):
#     print("Modem Manufacturer: ", modem.get_manufacturer())
#     print("Modem Signal: ", modem.get_signal_quality())
#     print("Modem Model: ", modem.get_model())

main()