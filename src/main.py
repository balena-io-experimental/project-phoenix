import gi

gi.require_version('GLib', '2.0')

from gi.repository import GLib
from balenaos import BalenaOS, OsNetwork

def main():
    #Create balenaOS singleton
    os = BalenaOS('OS dbus interface')
    net = OsNetwork('Network interface')
    
    #get a NM client
    nm = net.client
    
    #get a modem instance
    modem = net.modem

    #Show device and OS info
    os.print_os_info()
    #Show the current modem info
    net.print_modem_info()

    #listen for changes on the default connection
    nm.connect('notify::primary-connection', net.primary_connection_changed)

    #Listen for changes to connectivity level
    nm.connect('notify::connectivity', net.connectivity_changed)

    #Show primary connections IP address
    net.print_addresses(nm.get_primary_connection())

    print("connection state: ", net.get_connectivity_state())

    GLib.MainLoop().run()

main()