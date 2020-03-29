#!python3
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Example code to create a PyQt5 window.

Written for Python 3.

---
Authors: Ali H Al-Hakim
Date: 29 March 2020
"""
# Standard Library
import sys

# Third Party Library
from PyQt5 import QtCore, QtGui, QtWidgets


########################################################################
WINDOW_HEIGHT = 600 # in pixels
WINDOW_WIDTH = 1000 # in pixels

TITLE = "PyQt5 Template"
VERSION = "0.1.0"
DATE = "29 March 2020"

DIALOG_NAME_HELP_ABOUT = "Help About"


########################################################################
class MainWindow(QtWidgets.QMainWindow):
    """ The main application window
    """

    def __init__(self):
        super(MainWindow, self).__init__()

        # Configure basic MainWindow properties
        self.setWindowTitle("PyQt5 Example MainWindow")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Define class object handlers.
        self.dialogs = {}  # Dialog window object manager

        # Add a menu bar
        self.menubar = self.menuBar()
        self.menubar_fileMenu = self.menubar.addMenu("&File")
        action_fileExit = QtWidgets.QAction("&Exit", self)
        action_fileExit.triggered.connect(self.closeEvent)
        action_fileExit.setStatusTip('Exit application')
        self.menubar_fileMenu.addAction(action_fileExit)

        self.menubar_helpMenu = self.menubar.addMenu("&Help")
        action_helpAbout = QtWidgets.QAction("&About", self)
        action_helpAbout.triggered.connect(self.show_dialog_helpAbout)
        self.menubar_helpMenu.addAction(action_helpAbout)

        # Add a status bar
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setFixedWidth(self.width())
        self.statusBar().addWidget(self.statusbar)
        self.statusbar.showMessage("Statusbar message")

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

    #-------------------------------------------------------------------
    # METHODS
    #-------------------------------------------------------------------
    def show_dialog_helpAbout(self):
        """ Display a dialog window with information about the app.
        """
        print(self.dialogs)
        if DIALOG_NAME_HELP_ABOUT in self.dialogs:
            # Bring dialog forward and shift focus to it if it is open.
            self.dialogs[DIALOG_NAME_HELP_ABOUT].show()
            self.dialogs[DIALOG_NAME_HELP_ABOUT].activateWindow()
        else:
            # Create the dialog if it does not exist.
            dialog = DialogHelpAbout(self)
            dialog.show()
            self.dialogs[DIALOG_NAME_HELP_ABOUT] = dialog

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
        # Fix statusbar to the width of MainWindow
        self.statusbar.setFixedWidth(self.width())

    def closeEvent(self, event):
        """ Handle QObject close event (i.e. window is closed)
        """
        kill_list = []
        for name, dialog in self.dialogs.items():
            kill_list.append(name)
        for name in kill_list:
            print("Closing '{}' dialog".format(name))
            self.dialogs[name].close()
        print("Closing MainWindow")


########################################################################
class MainWidget(QtWidgets.QWidget):
    """
    A container inserted into the mainWindow for other widgets to be
    inserted into.
    """
    def __init__(self, parent):
        super(MainWidget, self).__init__(parent=parent)
        self.parent = parent

        self.principalLayout = QtWidgets.QHBoxLayout()
        self.principalLayout.addWidget(QtWidgets.QTextEdit("Free-form text field", self))
        self.setLayout(self.principalLayout)


########################################################################
class DialogHelpAbout(QtWidgets.QDialog):
    """ A dialog window to show information about the application
    """

    def __init__(self, parent):
        super(DialogHelpAbout, self).__init__(parent=parent)
        self.name = DIALOG_NAME_HELP_ABOUT
        self.parent = parent
        self.setWindowTitle("Help - About")
        self.setMinimumSize(250, 100)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Application: {}".format(TITLE)))
        layout.addWidget(QtWidgets.QLabel("Version: {}".format(VERSION)))
        layout.addWidget(QtWidgets.QLabel("Release Date: {}".format(DATE)))
        self.setLayout(layout)

    def closeEvent(self, event):
        """ Handle close event (i.e. window is closed)
        """
        self.parent.dialogs.pop(self.name)


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
    Window = MainWindow()
    Window.setMainWidget(MainWidget(Window))

    # Run the application
    Window.show()
    App.exec_()


########################################################################
if __name__ == "__main__":
    # Run the main application
    main()
