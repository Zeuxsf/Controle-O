#!/bin/bash
sleep 1
# Primeiro seta auto_exposure pra manual (1), DEPOIS seta a exposição
/usr/bin/v4l2-ctl -d /dev/video0 --set-ctrl=auto_exposure=1
sleep 0.5
/usr/bin/v4l2-ctl -d /dev/video0 --set-ctrl=exposure_time_absolute=80
# Resto dos controles
/usr/bin/v4l2-ctl -d /dev/video0 --set-ctrl=brightness=55
/usr/bin/v4l2-ctl -d /dev/video0 --set-ctrl=contrast=500
/usr/bin/v4l2-ctl -d /dev/video0 --set-ctrl=saturation=500
/usr/bin/v4l2-ctl -d /dev/video0 --set-ctrl=gamma=100
/usr/bin/v4l2-ctl -d /dev/video0 --set-ctrl=gain=5
/usr/bin/v4l2-ctl -d /dev/video0 --set-ctrl=power_line_frequency=2
/usr/bin/v4l2-ctl -d /dev/video0 --set-ctrl=white_balance_temperature=6500
/usr/bin/v4l2-ctl -d /dev/video0 --set-ctrl=sharpness=100
/usr/bin/v4l2-ctl -d /dev/video0 --set-ctrl=backlight_compensation=255
