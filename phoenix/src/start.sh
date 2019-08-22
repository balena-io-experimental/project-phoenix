#!/bin/bash

export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket 

echo "======================Phoenix========================="
python3 src/main.py

while true
do
	echo "Waiting in infinite loop..."
	sleep 30
done