#!/bin/bash

export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket 

echo "======================================================="
python3 src/main.py

while true
do
	echo "Press [CTRL+C] to stop.."
	sleep 30
done