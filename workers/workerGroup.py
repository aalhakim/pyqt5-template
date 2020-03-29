#!python3
#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Worker Object Code

Last Updated: 18 December 2019 (Ali Al-Hakim)
"""

# Standard Library Imports
import os
import time
import logging
debugLogger = logging.getLogger(__name__)

# Third-Part Library Imports
from PyQt5 import QtCore

# Local Library imports
from workers.controller import Controller
# from spinner import Spinner
from workers.webClient import WebClient


########################################################################
# Define a period of time to wait before force-killing all threads.
SHUTDOWN_DELAY = 0.1    # seconds

# Obtain S3 login credentials
import dotenv
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
S3_ACCESS_KEY = os.environ["S3_ACCESS_KEY"]
S3_SECRET_KEY = os.environ["S3_SECRET_KEY"]
S3_BUCKET = os.environ["S3_BUCKET"]

# Obtain Github access credentials
REPO_ACCESS_TOKEN = os.environ["REPO_ACCESS_TOKEN"]

########################################################################
class WorkerGroup(QtCore.QObject):

    # Define Signals
    sigStartController = QtCore.pyqtSignal()
    sigStartSpinner = QtCore.pyqtSignal()
    sigStartWebClient = QtCore.pyqtSignal()
    sigShutdown = QtCore.pyqtSignal()

    def __init__(self):
        super(WorkerGroup, self).__init__()
        self.threads = {}
        self.threads[self._create_controller()] = "Controller"
        self.threads[self._create_webClient()] = "WebClient"
        # self.threads[self._create_downloader()] = "downloader"
        # self.threads[self._create_uploader()] = "uploader"
        # self.threads[self._create_spinner()] = "spinner"

    def _create_controller(self):
        debugLogger.debug("Creating thread: Controller.")
        self.controller = Controller()
        self.controller_thread = QtCore.QThread()
        self.controller.moveToThread(self.controller_thread)
        self.controller_thread.start()
        return self.controller_thread

    def _create_webClient(self):
        debugLogger.debug("Creating thread: WebClient.")
        self.webClient = WebClient(S3_BUCKET, S3_ACCESS_KEY, S3_SECRET_KEY, REPO_ACCESS_TOKEN)
        self.webClient_thread = QtCore.QThread()
        self.webClient.moveToThread(self.webClient_thread)
        self.webClient_thread.start()
        return self.webClient_thread

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
