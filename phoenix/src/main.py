import gi, time

gi.require_version('GLib', '2.0')

from gi.repository import GLib
try:
    from balenaos import BalenaOS, OsNetwork
except:
    print("Error loading modules")

#Create balenaOS singleton
os = BalenaOS('OS dbus interface')
net = OsNetwork('Network interface')
#get a NM client
nm = net.client

def print_info():
    print("=======================================================\n")
    print("Connection State: ", net.get_connectivity_state())
    net.print_addresses(nm.get_primary_connection())
    net.print_modem_info()
    print("Connection Type: ", net.connectionType)
    return True

def main():

    #Show device and OS info
    os.print_os_info()
    
    #Listen for changes to connectivity level
    nm.connect('notify::connectivity', net.connectivity_changed)

    print_info()

    print("=======================================================\n")
    print("Active Connections:")
    activeConnections = nm.get_active_connections()
    net.print_active_connections(activeConnections)
    
    #periodically print info
    GLib.timeout_add_seconds(60, print_info)

    GLib.MainLoop().run()

main()