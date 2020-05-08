"""
Information about the application.
"""

# Standard library imports
import os
import sys
import uuid
import socket
import hashlib
import platform


########################################################################
PACKAGE_NAME = "pyqt5-template"
PACKAGE_DIRECTORY = __file__[0:__file__.find(PACKAGE_NAME)+len(PACKAGE_NAME)]
sys.path.append(PACKAGE_DIRECTORY)


def get_machine_id():
    """
    Obtain a unique ID for the PC running the script.
    """
    mac = str(uuid.getnode()).encode("utf-8")
    machine_id = hashlib.md5(mac).hexdigest()[0:8]
    return(machine_id)


########################################################################
# System Information
MACHINE_ID = get_machine_id()
OPERATING_SYSTEM = platform.system()  # 'Windows' for Windows, 'Linux' for Linux, 'Darwin' for OSX
HOSTNAME = socket.gethostname()


########################################################################
# Application Data
ORGANISATION_NAME = "Alpaca Apps Ltd"
APPLICATION_NAME = "PyQt5 Example Application"
VERSION = "0.1.0"
RELEASE_DATE = "04 April 2020"


########################################################################
# Action Names
ACTION_UPDATE_CONFIGURATION = "Update Configuration"


########################################################################
# Configuration Options
CONFIG_FILE = os.path.abspath(os.path.join(PACKAGE_DIRECTORY, "workers", "config.ini"))

CONFIG_VALIDATE_CRC = "Validate CRC"
CONFIG_VALIDATE_REGISTERED = "Validate Registered"
CONFIG_SOFTWARE_AUTOUPDATE = "Software Auto-Update"
CONFIG_SOFTWARE_LIST = "Software List"
CONFIG_PRINTER_AUTOSELECT = "Printer Auto-Select"
CONFIG_PRINTER_LIST = "Printer List"

CONFIGURATIONS = [
    CONFIG_VALIDATE_CRC,
    CONFIG_VALIDATE_REGISTERED,
    CONFIG_SOFTWARE_AUTOUPDATE,
    CONFIG_SOFTWARE_LIST,
    CONFIG_PRINTER_AUTOSELECT,
    CONFIG_PRINTER_LIST
]


########################################################################
# Dialog Window Names
DIALOG_NAME_HELP_ABOUT = "Help - About"
DIALOG_NAME_HELP_GUIDE = "Help - User Guide"


########################################################################
if __name__ == "__main__":
    print("OS: {}".format(OPERATING_SYSTEM))
    print("Hostname: {}".format(HOSTNAME))
    print("Machine ID: {}".format(MACHINE_ID))

    print ("Config File Location: {}".format(CONFIG_FILE))
