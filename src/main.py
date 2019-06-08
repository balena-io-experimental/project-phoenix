import gi

gi.require_version('GLib', '2.0')

from gi.repository import GLib
from balenaos import BalenaOS, OsNetwork

def main():
    #Create balenaOS singleton
    os = BalenaOS('OS dbus interface')
    net = OsNetwork('Network interface')
    
    #get a NM client
    client = net.client
    
    #get a modem instance
    modem = net.modem

    #Show device and OS info
    os.print_os_info()
    #Show the current modem info
    net.print_modem_info()

    #listen for changes on the default connection
    client.connect('notify::primary-connection', net.primary_connection_changed)
    primary_connection = client.get_primary_connection()

    net.print_addresses(primary_connection)

    GLib.MainLoop().run()

main()