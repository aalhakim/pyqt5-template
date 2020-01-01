#!/usr/bin/python
# -*- coding: utf-8 -*-

""" mainWindow.py
MainWindow PyQt5 object.

Last Updated: 18 December 2019 (Ali Al-Hakim)
"""

# Standard Library Imports
import os
import sys
import logging
debugLogger = logging.getLogger(__name__)

# Third-Party Library Imports
from PyQt5 import QtCore, QtGui, QtWidgets


########################################################################
WINDOW_WIDTH = 1280 # in pixels
WINDOW_HEIGHT = 720 # in pixels

ICON_FILE = "graphics/icon.png"

VERSION = 1


########################################################################
class MainWindow(QtWidgets.QMainWindow):
    """ The main application window
    """

    sigShutdown = QtCore.pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.debugMode = False

        # Configure basic MainWindow properties
        self.setWindowTitle("PyQt5 Example Application :: V{}".format(VERSION))
        print(os.path.join(os.path.dirname(__file__), os.path.normpath(ICON_FILE)))
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), ICON_FILE)))
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.centre()

        # Add a menubar, toolbars and status bar
        self.initStatusbar()

        # Add a central widget
        self.mainWidget = None

    #-------------------------------------------------------------------
    # METHODS
    #-------------------------------------------------------------------
    def initStatusbar(self):
        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.setSizeGripEnabled(False)
        self.status_bar.setFixedWidth(self.width())
        self.statusBar().addWidget(self.status_bar)
        self.status_bar.showMessage("Ready")

    def centre(self):
        """ Centre the window in any size monitor.
        """
        # Copy the geometry of the main window
        frameGm = self.frameGeometry()
        # Locate the centre point of the computer screen
        centre_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        # Move frameGm to the centre of the computer screen
        frameGm.moveCenter(centre_point)
        # Move the main window's top-left corner to match that of frameGm
        self.move(frameGm.topLeft())

    def setMainWidget(self, QWidget):
        """ Set the central widget of the main window widget.

        Args:
            QWidget: QWidget object to be set as the MainWindow central
                    widget

        Returns:
            Nothing. This method only sets the
        """
        self.mainWidget = QWidget
        self.setCentralWidget(self.mainWidget)

    @QtCore.pyqtSlot()
    def shutdown(self):
        """ Close the window and shutdown the application.

        This is used on top of the closeEvent method and is only called
        by the WorkerGroup object once all threads have been killed.
        """
        debugLogger.info("Shutdown complete")
        sys.exit(0)  # [AHA] Is this too brute force?

    #-------------------------------------------------------------------
    # EVENT HANDLERS
    #-------------------------------------------------------------------
    def keyPressEvent(self, event):
        """ Handle key press events

        Keys that can be handled are listed in the Qt5 docs:
          https://doc.qt.io/qt-5/qt.html#Key-enum
        """
        # Close MainWindow if the user presses ESC
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def resizeEvent(self, event):
        """ Actions if the MainWindow object gets resized
        """
        # Fix status_bar to the width of MainWindow
        self.status_bar.setFixedWidth(self.width())

    def closeEvent(self, event):
        """ Handle QObject close event (i.e. window is closed)
        """
        # TODO (AHA) There must be a neater way to shutdown the appliction with less dependancy on thread shutdown

        if self.debugMode is False:
            # Don't allow pyQt to close the Window (to ensure threads can be
            # dealt with first)
            event.ignore()

            # Configure all switches to off by interrupting all ongoing tests
            #debugLogger.info("Starting program shutdown.")
            debugLogger.info("Starting shutdown sequence.")
            self.sigShutdown.emit()

            # # Re-enable Raspberry Pi screen-blanking (i.e. screen-saver)
            # import os
            # os.system("xset s on; xset +dpms; xset s blank")
        else:
            debugLogger.warning("Closing window.\n")


########################################################################
if __name__ == "__main__":

    # Create the application
    App = QtWidgets.QApplication(sys.argv)

    # Create 'main' worker thread
    Window = MainWindow()
    Window.debugMode = True

    # Run the application
    Window.show()
    sys.exit(App.exec_())
