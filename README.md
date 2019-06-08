## TODO:
- add docker-compose.yml to demonstrate multicontainer use.
- Show primary interface name [link](https://lazka.github.io/pgi-docs/#NM-1.0/classes/Connection.html#NM.Connection.get_interface_name)
- Show primary connection type (eth, wifi or gsm) [link](https://lazka.github.io/pgi-docs/#NM-1.0/classes/ActiveConnection.html#NM.ActiveConnection.get_connection_type)
- If connectivity state is UNKNOWN, try restart NM.
- function to add new wifi connection [link](https://lazka.github.io/pgi-docs/#NM-1.0/classes/Client.html#NM.Client.add_and_activate_connection_async)
- function to add new cellular connection
- add checkpoint and rollback functionality when switching between network profile, [create](https://lazka.github.io/pgi-docs/#NM-1.0/classes/Client.html#NM.Client.checkpoint_create) and [rollback](https://lazka.github.io/pgi-docs/#NM-1.0/classes/Client.html#NM.Client.checkpoint_rollback)

## Links
https://wiki.freedesktop.org/www/Software/systemd/dbus/ 
https://lazka.github.io/pgi-docs/#NM-1.0
https://lazka.github.io/pgi-docs/#ModemManager-1.0