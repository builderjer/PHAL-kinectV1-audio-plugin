from os import environ
from os.path import isfile, isdir, abspath, dirname, basename
from subprocess import run, PIPE
from ovos_utils.log import LOG

SCRIPT_BIN_PATH = "/usr/bin/ovos_kinect_upload_fw"
SCRIPT_FIRMWARE_PATH = "/usr/local/share/kinect/UACFirmware"

def _check_for_bin(path_to_bin=None):
    bin_path = path_to_bin or SCRIPT_BIN_PATH
    return isfile(path_to_bin)

def install_bin_script(install_path=None):
    install_path = install_path or SCRIPT_BIN_PATH
    local_bin_script = abspath(dirname(__file__) + "/overlays/usr/bin/ovos_kinect_upload_fw")
    if not _check_for_bin(install_path):
        # Check for /usr/bin
        if not isdir(dirname(install_path)):
            x = run(f'sudo mkdir -p {dirname(install_path)}', shell=True, capture_output=True)
            if x.returncode != 0:
                LOG.error(f"Could not create directory {dirname(install_path)}: {x.stderr.strip().decode()}")
                return False
        x = run(f'sudo cp {local_bin_script} {install_path}', shell=True, capture_output=True)
        if x.returncode != 0:
            LOG.error(f"Could not copy bin to {install_path}: {x.stderr.strip().decode()}")
            return False
        x = run(f'sudo chmod a+x {install_path}', shell=True, capture_output=True)
        if x.returncode != 0:
            LOG.error(f"Could not make the bin executable: {x.stderr.strip().decode()}")
            return False
    return True

def _check_for_fw(path_to_fw=None):
    fw_dir = path_to_fw or SCRIPT_FIRMWARE_PATH
    return isfile(fw_dir)

def install_fw(install_path=None):
    install_path = install_path or SCRIPT_FIRMWARE_PATH
    local_fw = abspath(dirname(__file__) + "/firmware/UACFirmware")
    if not _check_for_fw(install_path):
        if not isdir(dirname(install_path)):
            x = run(f"sudo mkdir -p {dirname(install_path)}", shell=True, capture_output=True)
            if x.returncode != 0:
                LOG.error(f"Could not create directory for firmware: {x.stderr.strip().decode()}")
                return False
        x = run(f"sudo cp {local_fw} {install_path}", shell=True, capture_output=True)
        if x.returncode != 0:
            LOG.error(f"Could not copy firmware file to {install_path}: {x.stderr.strip().decode()}")
            return False
        x = run(f"sudo chmod 655 {install_path}", shell=True, capture_output=True)
        if x.returncode != 0:
            LOG.error(f"Could not create correct permisions for firmware: {x.stderr.strip().decode()}")
            return False
    return True

def upload_fw(bin_path=None, fw_path=None):
    bin_path = bin_path or SCRIPT_BIN_PATH
    fw_path = fw_path or SCRIPT_FIRMWARE_PATH
    print(f"xxxxxxxx {bin_path} {fw_path}")
    x = run(f"sudo {bin_path} {fw_path}", shell=True, capture_output=True)
    if x.returncode !=0:
        LOG.error(f"Could not upload fw to Kinect:  {x.stderr}")
        return False
    LOG.info("Uploaded fw to Kinect")
    return True

def check_for_path():
    x = run("ovos_kinect_fw", shell=True, capture_output=True)
    if x.returncode != 0:
        # ovos_kinect_fw is not in PATH
        x = run(f"sudo ln -s /home/mycroft/.local/bin/ovos_kinect_fw /usr/bin", shell=True, capture_output=True)
        if x.returncode != 0:
            LOG.error(f"Could not create systemlink: {x.stderr.strip().decode()}")
            return False
        LOG.info("Created systemlink in /usr/bin")
    return True
