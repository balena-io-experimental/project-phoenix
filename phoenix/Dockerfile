FROM balenalib/raspberrypi3-alpine:edge

RUN apk add python3 \
    networkmanager \
    modemmanager \
    py3-gobject3 \
    py3-dbus

COPY . .

CMD [ "bash", "src/start.sh" ]