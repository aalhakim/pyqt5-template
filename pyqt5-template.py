#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The main executable file for the Elohmir database program

Authors: Ali H Al-Hakim
Date: 29 September 2018
"""
# Standard Library
import sys

# Third Party Library
from PyQt5 import QtCore, QtGui, QtWidgets


########################################################################
WINDOW_HEIGHT = 600 # in pixels
WINDOW_WIDTH = 1000 # in pixels


########################################################################
class MainWindow(QtWidgets.QMainWindow):
    """ The main application window
    """

    def __init__(self):
        super(MainWindow, self).__init__()

        # Configure basic MainWindow properties
        self.setWindowTitle("PyQt5 Example MainWindow")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Add a status bar
        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.setSizeGripEnabled(False)
        self.status_bar.setFixedWidth(self.width())
        self.statusBar().addWidget(self.status_bar)
        self.status_bar.showMessage("Ready")

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
        print("Closing MainWindow")


########################################################################
def close_app():
    """ Actions prior to the application being shutdown
    """
    print("Closing Application")


########################################################################
def main():
    # Create the main application window object
    App = QtWidgets.QApplication(sys.argv)

    # Connect the application to the close_app function for elegant
    # handling of program closing.
    App.aboutToQuit.connect(close_app)

    # Create the MainWindow object
    window = MainWindow()
    window.show()

    # Run the application
    App.exec_()


########################################################################
if __name__ == "__main__":
    # Run the main application
    main()
