from os.path import isfile, isdir, abspath, dirname
from subprocess import run
from ovos_utils.log import LOG

UDEV_RULES_PATH = "/etc/udev/rules.d/55-ovos-kinect-audio.rules"

def _check_for_rules(path_to_rule=None):
    path_to_rule = path_to_rule or UDEV_RULES_PATH
    return isfile(path_to_rule)

def install_rules(path_to_rule=None):
    path_to_rule = path_to_rule or UDEV_RULES_PATH
    if not _check_for_rules(path_to_rule):
        local_rule = abspath(dirname(__file__) + "/overlays/etc/udev/rules.d/55-ovos-kinect_audio.rules")
        if not isdir(dirname(path_to_rule)):
            x = run(f"sudo mkdir -p {path_to_rule}", shell=True, capture_output=True)
            if x.returncode !=0:
                LOG.error(f"Cannot create rule directory: {x.stderr.strip().decode()}")
                return False
        x = run(f"sudo cp {local_rule} {path_to_rule}", shell=True, capture_output=True)
        if x.returncode != 0:
            LOG.error(f"Cannot copy rules to file: {x.stderr.strip().decode()}")
            return False
        x = run(f"sudo udevadm control --reload && sudo udevadm trigger", shell=True, capture_output=True)
        if x.returncode != 0:
            LOG.error(f"Cannot reload udev: {x.stderr.strip().decode()}")
            return False

    return True

