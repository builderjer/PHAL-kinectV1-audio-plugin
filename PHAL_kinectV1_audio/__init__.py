from subprocess import run, PIPE
from os import environ

import click

from ovos_plugin_manager.phal import PHALPlugin
from ovos_utils.log import LOG

from PHAL_kinectV1_audio.udev import install_rules
from PHAL_kinectV1_audio.fw import install_bin_script, install_fw

OVOS_KINECT_FW_OPTIONS = ['add', 'remove', 'upload']

@click.command()
@click.argument("command", type=click.Choice(OVOS_KINECT_FW_OPTIONS, case_sensitive=False))
@click.option("--bin-path", default=None, help="path to fw upload bin")
@click.option("--fw-path", default=None, help="path to fw")
def ovos_kinect_fw(command, bin_path, fw_path):
    if command in OVOS_KINECT_FW_OPTIONS:

        pulse_source = "alsa_input.usb-Microsoft_Kinect_USB_Audio_B44886513430049B-01.input-4-channels"
        if command == "add":
            LOG.info("adding firmware and pulse files")
            x = run("pactl get-default-source", shell=True, capture_output=True)
            if x.returncode != 0:
                LOG.error(f"No default source for pulse: {x.stderr.strip().decode()}")
            else:
                try:
                    environ["ORIG_PULSE_DEFALUT_SOURCE"] = x.stdout.strip().decode()
                    LOG.debug(f"Saved environ['ORIG_PULSE_DEFALUT_SOURCE'] as {x.stdout.strip().decode()}")
                except Exception as e:
                    LOG.error(f"Could not save origional pulse source: {e}")

            x = run(f"pactl set-default-source {pulse_source}", shell=True, capture_output=True)
            if x.returncode != 0:
                LOG.error(f"Cannot set default source: {x.stderr.strip().decode()}")

        elif command == "remove":
            LOG.info("removing pulse files")
            LOG.debug(environ["ORIG_PULSE_DEFALUT_SOURCE"])
            x = run(f"pactl set-default-source {environ['ORIG_PULSE_DEFALUT_SOURCE']}", shell=True, stdout=PIPE, stderr=PIPE)
            if x.returncode != 0:
                LOG.error(f"Cannot set default source: {x.stderr.strip().decode()}")

        elif command == "upload":
            LOG.info("uploading firmware to kinect")
            if upload_fw(bin_path, fw_path):
                ovos_kinect_fw("add", bin_path, fw_path)


class KinectAudioPlugin(PHALPlugin):
    def __init__(self, bus=None, config=None):
        super().__init__(bus, 'phal-kinectV1', config)
        rule_path = self.config.get("rule_path")
        bin_path = self.config.get("bin_path")
        fw_path = self.config.get("fw_path")
        if install_rules(rule_path):
            LOG.debug(f"Installed rules to {rule_path}")
        if install_bin_script(bin_path):
            LOG.debug(f"Installed bin to {bin_path}")
        if install_fw(fw_path):
            LOG.debug(f"Installed fw to {fw_path}")

