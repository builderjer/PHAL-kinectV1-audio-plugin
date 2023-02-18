# Kinect Xbox V.1 audio plugin

[There is a bug](#Bugs) that does not allow the firmware to upload on connection of the Kinect. 

[Open Issue](https://github.com/builderjer/PHAL-kinectV1-audio-plugin/issues/1}

This plugin allows the Microsoft Kinect V.1 to be used as a microphone with OVOS
It <strong>DOES NOT</strong> or is not needed with the windows verion of the Kinect.
This is for a USB/12v modified version of the origional Xbox Kinect.

## How to install

`git clone https://github.com/builderjer/PHAL-kinectV1-audio-plugin`

`pip install ./PHAL-kinectV1-audio-plugin`

restart OVOS to load plugin

[Bug fix to enable kinect](#Bugs)

### Install Overview

This software installs the following files

<strong>This assumes the user mycroft and will need modified if the default user is other than that</strong>

`/usr/bin/kinect_upload_fw`
  - This is the binary that actually installs the firmware to the Kinect when attached

`/usr/local/share/kinect/UACFirmware`
  - This is the firmware that gets loaded to the device

`/etc/udev/rules.d/55-kinect_audio.rules`
  - The udev rules to upload firmware and allow regular user to use

#### When installed with pip

`ovos_kinect_fw`
  - Run without arguments for help

## Acknowledgments

https://github.com/dev-0x7C6/kinect-audio-setup
  - The bin to upload to the kinect

https://github.com/dev-0x7C6/kinect-audio-firmware
  - Actual firmware for the kinect

### Bugs

udev rule does not load when the device is plugged in.  In order to upload the firmware, after plugging in the Kinect, run the command `ovos_kinect_fw upload` and the Kinect should be working as the microphone

[Open Issue](https://github.com/builderjer/PHAL-kinectV1-audio-plugin/issues/1}
