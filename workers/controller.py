#!python3

"""
Application main control code

Last Updated: 05 April 2020 (Ali Al-Hakim)
"""

import sys
if __name__ == "__main__":
    pkg_name = "pyqt5-template"
    pkg_dir = __file__[0:__file__.find(pkg_name)+len(pkg_name)]
    sys.path.append(pkg_dir)

# Standard library imports
import os
import time
import logging
import configparser
debugLogger = logging.getLogger(__name__)

# Third-party library imports
from PyQt5 import QtCore

# Local library imports
from modules import appdata


########################################################################
class Controller(QtCore.QObject):

    sigShutdown = QtCore.pyqtSignal()
    sigReleaseQuery = QtCore.pyqtSignal(str)
    sigEnableApplication = QtCore.pyqtSignal(bool)
    sigUpdateApplication = QtCore.pyqtSignal(str)
    sigUpdateSoftwareList = QtCore.pyqtSignal(list)
    sigUpdateConfigStatus = QtCore.pyqtSignal(str, bool)

    def __init__(self):
        super(Controller, self).__init__()
        self.daemon = True


    ####################################################################
    # THREAD MANAGEMENT
    ####################################################################
    @QtCore.pyqtSlot()
    def start(self):
        """
        Initialise controller worker.
        """
        debugLogger.debug("Starting controller worker.")
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._update)    # Run this function
        # ------------- #
        # Do setup here #
        # ------------- #
        self._start_loop()

    def _update(self):
        """
        Listen for input and respond
        """

        # ---------------------- #
        # Respond to inputs here #
        # ---------------------- #

        # Wait and then re-trigger the timer to run through the loop again
        time.sleep(0.2)
        self.timer.start(0)

    def _start_loop(self):
        """
        Start the perpetual loop.
        """
        debugLogger.info(" Starting controller loop.")
        self.timer.start()                          # Re-run the timer

    def _stop_loop(self):
        """
        Stop the perpetual loop.
        """
        debugLogger.debug(" Stopping controller loop")
        self.timer.stop()


    @QtCore.pyqtSlot()
    def shutdown(self):
        """
        Begin the shutdown sequence for this thread.
        """
        # -------------------------- #
        # Kill active processes here #
        # -------------------------- #
        self.sigShutdown.emit()

    ####################################################################
    # METHODS
    ####################################################################
    @QtCore.pyqtSlot(str)
    def handle_release_latest(self, tag_name):
        """
        Handle receipt of latest release tag data.
        """
        self.latest_release = tag_name

    @QtCore.pyqtSlot(list)
    def handle_release_list(self, tag_names):
        """
        Handle receipt of release list data
        """
        self.software_list = tag_names
        print(tag_names)

    @QtCore.pyqtSlot()
    def handle_update_configuration(self):
        """
        Update configuration settings.
        """
        new_settings = {}

        self.config = configparser.ConfigParser()
        self.config.optionxform = str  # Don't force option names to lowercase.
        self.config.read(appdata.CONFIG_FILE)

        sections = self.config.sections()
        if "master" in sections:
            for option in self.config["master"]:
                new_settings[option] = self._extract_configuration("master", option)

        hostname = appdata.HOSTNAME
        if hostname in sections:
            for option in self.config[hostname]:
                new_settings[option] = self._extract_configuration(hostname, option)

        print(new_settings)

        if "enabled" in new_settings:
            if new_settings["enabled"] is not None:
                self.sigEnableApplication.emit(new_settings["enabled"])

        if "updateList" in new_settings:
            self.sigUpdateSoftwareList.emit(new_settings["updateList"])

        if "autoUpdate" in new_settings:
            if new_settings["autoUpdate"] is not None:
                self.sigUpdateConfigStatus.emit(appdata.CONFIG_SOFTWARE_AUTOUPDATE, new_settings["autoUpdate"])
                if new_settings["autoUpdate"] is True and "autoUpdateVersion" in new_settings:
                    self.sigUpdateApplication.emit(new_settings["autoUpdateVersion"])

        if "defaultLanguage" in new_settings:
            if new_settings["defaultLanguage"] is not None:
                debugLogger.error("This function has not been written yet")



    def _extract_configuration(self, section, option):
        """
        Return the configuration value in the correct format.

        Parameters
        ==========
        section: <string>
            The section of the INI file the key is found in.
        option: <string>
            The name of the property of interest.
        """
        value_str = str(self.config[section][option]).lower()
        if value_str == "null":
            value = None

        elif value_str == "[]":
            value = []

        else:
            if option == "enabled":
                value = self.config[section].getboolean(option)

            elif option == "autoUpdate":
                value = self.config[section].getboolean(option)

            elif option == "autoUpdateVersion":
                value = value_str

            elif option == "defaultLanguage":
                value = value_str

            elif option == "updateList":
                value = [item.strip() for item in value_str.strip("[").strip("]").split(",")]

            else:
                debugLogger.warning("Unhandled configuration passed as <str>: {} = '{}'".format(option, value_str))
                value = value_str

        return value


if __name__ == "__main__":
    controller = Controller()
    controller.handle_update_configuration()
