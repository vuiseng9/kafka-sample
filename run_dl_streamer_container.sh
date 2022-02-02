#!/usr/bin/env bash

container=openvino/ubuntu18_data_dev:2021.4.2

xhost local:root

docker run -it \
    --net=host \
    -d \
    -u 0 \
    --device /dev/dri:/dev/dri \
    -v ~/.Xauthority:/root/.Xauthority \
    -v /tmp/.X11-unix/:/tmp/.X11-unix/ \
    -v /dev/bus/usb:/dev/bus/usb \
    -e DISPLAY=$DISPLAY \
    -v ${HOME}:/hosthome \
    ${container} bash
