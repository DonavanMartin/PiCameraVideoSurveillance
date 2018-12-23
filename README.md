# PiCameraVideoSurveillance
Basic spy camera using Raspberry Pi Zero with PiCamera and python3.


## Start at boot
$ sudo nano /etc/rc.local
-->Add line:
python3 /home/pi/camera.py &
