# Kinect Xbox V.1 audio plugin

This plugin allows the Microsoft Kinect V.1 to be used as a microphone with OVOS
It <strong>DOES NOT</strong> or is not needed with the windows verion of the Kinect.
This is for a USB/12v modified version of the origional Xbox Kinect.

### Install Overview

This software installs the following files

<strong>This assumes the user mycroft and will need modified if the default user is other than that</strong>

`/usr/local/bin/ovos_kinect_fw`
  - Helper script to upload firmware, install udev rules, and pulseaudio junk

`/usr/local/bin/kinect_upload_fw`
  - This is the binary that actually installs the firmware to the Kinect when attached

`/usr/local/bin/pulse_kinect_add`
  - Sets the pulseaudio default source to the Kinect device

`~/.local/bin/pulse_kinect_remove`
  - Removes the Kinect as the default device and restores back to OVOS default

`~/.local/share/kinect/firmware/UACFirmware`
  - This is the firmware that gets loaded to the device

`/lib/udev/rules.d/55-kinect_audio.rules`
  - The udev rules to upload firmware and allow regular user to use





