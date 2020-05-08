#!python3
#!/usr/bin/python
# -*- coding: utf-8 -*-

""" PyQt5 Example Application

Written By: Ali Al-Hakim
Last Updated: 18 December 2019
"""

# Logger configuration
if __name__ == "__main__":
    from logger.logging_config import config
    import logging.config
    logging.config.dictConfig(config)


# Standard Library Imports
import sys
import traceback
import logging
debugLogger = logging.getLogger(__name__)

# Third-Party Library Imports
from PyQt5 import QtCore, QtGui, QtWidgets

# Local Library Imports
from views.mainWindow import MainWindow
from views.centralWidget import CentralWidget
from workers.workerGroup import WorkerGroup


########################################################################
def connect_signals_and_slots(Window, Workers):
    """ Connect application signals and slots together.

    [Args]
    window: PyQt5.QtWidgets.QMainWindow object
    workers: workers.workerGroup.WorkerGroup object
    """
    # Connect WorkerGroup signals to application slots
    Workers.sigStartController.connect(Workers.controller.start)

    Workers.controller.sigReleaseQuery.connect(Workers.webClient.handle_release_query)
    Workers.webClient.sigReleaseLatest.connect(Workers.controller.handle_release_latest)
    Workers.webClient.sigReleaseList.connect(Workers.controller.handle_release_list)


def close_app():
    """ Actions prior to the application being shutdown
    """
    print("Closing Application")


########################################################################
def run_app():
    """ Run the application and display the main window.
    """
    try:
        # Create the main application window object
        App = QtWidgets.QApplication(sys.argv)

        # Connect the application to the close_app function for elegant
        # handling of program closing.
        App.aboutToQuit.connect(close_app)

        # Create functional worker threads
        Workers = WorkerGroup()

        # Create the MainWindow object (which is also the UI worker thread)
        Window = MainWindow()
        Window.setMainWidget(CentralWidget(Window))

        # Define signal-slot shutdown sequence
        Window.sigShutdown.connect(Workers.controller.shutdown)           # 1. End all control operations
        Workers.controller.sigShutdown.connect(Workers.kill_all_threads)  # 2. Kill all threads
        Workers.sigShutdown.connect(Window.shutdown)                      # 3. Close window

        # Connect other worker signals and slots together
        connect_signals_and_slots(Window, Workers)

        # Run the application
        Workers.sigStartController.emit()
        Workers.sigStartWebClient.emit()
        Window.show()
        App.exec_(App.exec_())

    except Exception:
        # Capture all application errors to ensure the worker threads
        # can then be killed in a controlled manner.
        debugLogger.error("There was a fatal error which caused the application to close.")
        traceback.print_exc()
        Workers.controller.closeEvent()
        Workers.kill_all_threads()


########################################################################
if __name__ == "__main__":
    # Run the main application
    run_app()
