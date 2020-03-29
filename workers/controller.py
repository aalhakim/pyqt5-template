#!python3

"""
Application main control code

Last Updated: 29 March 2020 (Ali Al-Hakim)
"""

# Standard library Imports
import os
import time
import logging
debugLogger = logging.getLogger(__name__)

# Third-Party Library Imports
from PyQt5 import QtCore


########################################################################
class Controller(QtCore.QObject):

    sigShutdown = QtCore.pyqtSignal()
    sigReleaseQuery = QtCore.pyqtSignal(str)

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
        time.sleep(0.05)
        self.timer.start(0)

    def _start_loop(self):
        """
        Start the perpetual loop.
        """
        debugLogger.info(" Starting controller loop.")
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._update)    # Run this function
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
