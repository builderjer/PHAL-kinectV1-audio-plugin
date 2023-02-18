from subprocess import run, PIPE
from os import environ

import click

from ovos_plugin_manager.phal import PHALPlugin
from ovos_utils.log import LOG

from PHAL_kinectV1_audio.udev import install_rules
from PHAL_kinectV1_audio.fw import install_bin_script, install_fw, check_for_path, upload_fw

OVOS_KINECT_FW_OPTIONS = ['add', 'remove', 'upload']

@click.command()
@click.argument("command", type=click.Choice(OVOS_KINECT_FW_OPTIONS, case_sensitive=False))
@click.option("--bin-path", default=None, help="path to fw upload bin")
@click.option("--fw-path", default=None, help="path to fw")
def ovos_kinect_fw(command, bin_path, fw_path):
    # When Python 3.10 is standard, this can change to a switch
    if command in OVOS_KINECT_FW_OPTIONS:
        if command == "add":
            LOG.info("adding firmware and pulse files")
            x = run("pactl get-default-source", shell=True, capture_output=True)
            if x.returncode != 0:
                LOG.debug(f"No default source for pulse: {x.stderr.strip().decode()}")
            else:
                try:
                    environ["ORIG_PULSE_DEFALUT_SOURCE"] = x.stdout.strip().decode()
                    LOG.debug(f"Saved environ['ORIG_PULSE_DEFALUT_SOURCE'] as {x.stdout.strip().decode()}")
                except Exception as e:
                    environ["ORIG_PULSE_DEFALUT_SOURCE"] = "OpenVoiceOS.monitor"
                    LOG.error(f"Could not save origional pulse source: {e}")
            # Get the device name
            x = run("pactl list sources", shell=True, capture_output=True)
            if x.returncode != 0:
                LOG.error(f"Error getting pulse sources: {x.stderr.strip().decode()}")
                return False
            x = x.stdout.decode()
            x = x.splitlines()
            for line in x:
                if "Name:" in line:
                    if "Kinect_USB_Audio" in line:
                        line = line.strip()
                        line = line[6:]
                        x = run(f"pactl set-default-source {line}", shell=True, capture_output=True)
                        if x.returncode != 0:
                            LOG.error(f"Cannot set default source: {x.stderr.strip().decode()}")
                        else:
                            LOG.info(f"Set pulse default source to {line}")

        elif command == "remove":
            LOG.info("removing pulse files")
            LOG.debug(environ["ORIG_PULSE_DEFALUT_SOURCE"])
            x = run(f"pactl set-default-source {environ['ORIG_PULSE_DEFALUT_SOURCE']}", shell=True, stdout=PIPE, stderr=PIPE)
            if x.returncode != 0:
                LOG.error(f"Cannot set default source: {x.stderr.strip().decode()}")

        elif command == "upload":
            LOG.info("uploading firmware to kinect")
            if upload_fw(bin_path, fw_path):
                LOG.debug("kinect firmware uploaded")
                x = run("ovos_kinect_fw add", shell=True, capture_output=True)
                if x.returncode != 0:
                    LOG.error(f"error after upload: {x.stderr.strip().decode()}")
                    return False
            return True


class KinectAudioPlugin(PHALPlugin):
    def __init__(self, bus=None, config=None):
        super().__init__(bus, 'phal-kinectV1', config)
        rule_path = self.config.get("rule_path")
        bin_path = self.config.get("bin_path")
        fw_path = self.config.get("fw_path")
        if install_rules(rule_path):
            LOG.debug("Installed rules")
        if install_bin_script(bin_path):
            LOG.debug("Installed bin")
        if install_fw(fw_path):
            LOG.debug("Installed fw")

