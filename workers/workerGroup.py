#!python3
#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Worker Object Code

Last Updated: 18 December 2019 (Ali Al-Hakim)
"""

# Standard Library Imports
import time
import logging
debugLogger = logging.getLogger(__name__)

# Third-Part Library Imports
from PyQt5 import QtCore

# Local Library imports
from workers.controller import Controller


########################################################################
# Define a period of time to wait before force-killing all threads.
SHUTDOWN_DELAY = 0.1    # seconds


########################################################################
class WorkerGroup(QtCore.QObject):

    # Define Signals
    sigStartController = QtCore.pyqtSignal()
    sigStartSpinner = QtCore.pyqtSignal()
    sigShutdown = QtCore.pyqtSignal()

    def __init__(self):
        super(WorkerGroup, self).__init__()
        self.threads = {}
        self.threads[self._create_controller()] = "controller"
        # self.threads[self._create_downloader()] = "downloader"
        # self.threads[self._create_uploader()] = "uploader"
        # self.threads[self._create_spinner()] = "spinner"

    def _create_controller(self):
        debugLogger.debug("Creating thread: controller.")
        self.controller = Controller()
        self.controller_thread = QtCore.QThread()
        self.controller.moveToThread(self.controller_thread)
        self.controller_thread.start()
        return self.controller_thread

    # def _create_spinner(self):
    #     debugLogger.debug("Creating thread: spinner.")
    #     self.spinner = Spinner()
    #     self.spinner_thread = QtCore.QThread()
    #     self.spinner.moveToThread(self.spinner_thread)
    #     self.spinner_thread.start()
    #     return self.spinner_thread

    @QtCore.pyqtSlot(str, str)
    def logger(self, priority, message):
        if priority == "debug":
            debugLogger.debug(message)
        elif priority == "info":
            debugLogger.info(message)
        elif priority == "warn":
            debugLogger.warn(message)
        elif priority == "error":
            debugLogger.error(message)

    @QtCore.pyqtSlot(QtCore.QThread)
    def reset_thread(self, thread):
        debugLogger.debug("Resetting thread {}.".format(thread))
        if thread.isRunning():
            thread.terminate()
            thread.wait()
            thread.start()
        debugLogger.debug("Thread {} reset.".format(thread))

    @QtCore.pyqtSlot(QtCore.QThread)
    def kill_thread(self, thread):
        debugLogger.debug("Terminating thread {}.".format(thread))
        if thread.isRunning():
            thread.terminate()
            thread.wait()
        debugLogger.debug("Thread {} terminated.".format(thread))

    @QtCore.pyqtSlot()
    def kill_all_threads(self):
        debugLogger.debug("Killing all threads.")
        # Give the controller some time to end
        time.sleep(SHUTDOWN_DELAY)
        # Kill all threads
        for thread, name in self.threads.items():
            if thread.isRunning():
                debugLogger.debug(" - Terminating thread {}.".format(name))
                thread.terminate()
                #thread.wait()
            debugLogger.debug(" - {} thread terminated".format(name))

        self.sigShutdown.emit()
