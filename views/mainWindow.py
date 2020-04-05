#!python3
#!/usr/bin/python
# -*- coding: utf-8 -*-

""" mainWindow.py
MainWindow PyQt5 object.

Last Updated: 18 December 2019 (Ali Al-Hakim)
"""

import sys
if __name__ == "__main__":
    pkg_name = "pyqt5-template"
    pkg_dir = __file__[0:__file__.find(pkg_name)+len(pkg_name)]
    sys.path.append(pkg_dir)

# Standard Library imports
import os
import logging
debugLogger = logging.getLogger(__name__)

# Third-Party Library imports
from PyQt5 import QtCore, QtGui, QtWidgets

# Local library imports
from modules import appdata
from views.dialogHelpAbout import DialogHelpAbout
from views.dialogHelpGuide import DialogHelpGuide


########################################################################
WINDOW_WIDTH = 1280 # in pixels
WINDOW_HEIGHT = 720 # in pixels

ICON_FILE = "graphics/icon.png"


########################################################################
class MainWindow(QtWidgets.QMainWindow):
    """ The main application window
    """

    sigShutdown = QtCore.pyqtSignal()
    sigUpdateConfiguration = QtCore.pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.debugMode = False

        # Define class object handlers.
        self.dialogs = {}  # Dialog window object manager
        self.software_list = []
        self.printer_list = []

        # Configure basic MainWindow properties
        self.setWindowTitle("{}  –  {}  –  v{}".format(appdata.ORGANISATION_NAME,
                                                       appdata.APPLICATION_NAME,
                                                       appdata.VERSION))
        print(os.path.join(os.path.dirname(__file__), os.path.normpath(ICON_FILE)))
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), ICON_FILE)))
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.centre()

        # Add a menubar, toolbars and status bar
        self.initMenubar()
        self.initStatusbar()

        # Add a central widget
        self.mainWidget = None

    #-------------------------------------------------------------------
    # METHODS
    #-------------------------------------------------------------------
    def initMenubar(self):
        """
        Draw a menubar along the top of the window
        """
        self.menubar = self.menuBar()

        # --- File Menu
        self.menubar_fileMenu = self.menubar.addMenu("&File")
        action_fileExit = QtWidgets.QAction("&Exit", self)
        action_fileExit.triggered.connect(self.closeEvent)
        action_fileExit.setStatusTip('Exit application')
        self.menubar_fileMenu.addAction(action_fileExit)

        # Application Configuration Menu
        self.menubar_configMenu = self.menubar.addMenu("&Configuration")
        action_updateConfiguration = QtWidgets.QAction("&Update Configuration", self)
        action_updateConfiguration.triggered.connect(self.sigUpdateConfiguration.emit)
        config_SoftwareAutoUpdate = QtWidgets.QAction("Software Auto-Update", self)
        config_SoftwareAutoUpdate.setEnabled(False)
        config_softwareUpdateList = QtWidgets.QMenu("Software Update List", self)
        config_validateCRC = QtWidgets.QAction("Validate CRC", self)
        config_validateCRC.setEnabled(False)
        config_validateRegistered = QtWidgets.QAction("Validate Registered", self)
        config_validateRegistered.setEnabled(False)

        self.menubar_configMenu.addAction(action_updateConfiguration)
        self.menubar_configMenu.addSeparator()
        self.menubar_configMenu.addAction(config_SoftwareAutoUpdate)
        self.menubar_configMenu.addMenu(config_softwareUpdateList)
        self.menubar_configMenu.addSeparator()
        self.menubar_configMenu.addAction(config_validateCRC)
        self.menubar_configMenu.addAction(config_validateRegistered)

        # Services Settings Menu
        self.menubar_servicesMenu = self.menubar.addMenu("&Services")
        config_autoSelectPrinter = QtWidgets.QAction("Auto-Select Printer", self)
        config_autoSelectPrinter.setEnabled(False)
        config_printerList = QtWidgets.QMenu("Printer List", self)

        self.menubar_servicesMenu.addAction(config_autoSelectPrinter)
        self.menubar_servicesMenu.addMenu(config_printerList)

        # Help Menu
        self.menubar_helpMenu = self.menubar.addMenu("&Help")
        action_helpGuide = QtWidgets.QAction("&Guide", self)
        action_helpGuide.triggered.connect(self.show_dialog_helpGuide)
        action_helpAbout = QtWidgets.QAction("&About", self)
        action_helpAbout.triggered.connect(self.show_dialog_helpAbout)

        self.menubar_helpMenu.addAction(action_helpGuide)
        self.menubar_helpMenu.addAction(action_helpAbout)

    def initStatusbar(self):
        """
        Draw a statusbar along the bottom of the window
        """
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
    # METHODS
    #-------------------------------------------------------------------
    def show_dialog_helpAbout(self):
        """ Display a dialog window with information about the app.
        """
        if appdata.DIALOG_NAME_HELP_ABOUT in self.dialogs:
            # Bring dialog forward and shift focus to it if it is open.
            self.dialogs[appdata.DIALOG_NAME_HELP_ABOUT].show()
            self.dialogs[appdata.DIALOG_NAME_HELP_ABOUT].activateWindow()
        else:
            # Create the dialog if it does not exist.
            dialog = DialogHelpAbout(self)
            dialog.show()
            self.dialogs[appdata.DIALOG_NAME_HELP_ABOUT] = dialog

    def show_dialog_helpGuide(self):
        """ Display a dialog window with information on how to use the app.
        """
        if appdata.DIALOG_NAME_HELP_GUIDE in self.dialogs:
            # Bring dialog forward and shift focus to it if it is open.
            self.dialogs[appdata.DIALOG_NAME_HELP_GUIDE].show()
            self.dialogs[appdata.DIALOG_NAME_HELP_GUIDE].activateWindow()
        else:
            # Create the dialog if it does not exist.
            dialog = DialogHelpGuide(self)
            dialog.show()
            self.dialogs[appdata.DIALOG_NAME_HELP_GUIDE] = dialog

    @QtCore.pyqtSlot(dict)
    def handle_update_configuration(self, config):
        """
        Update the widgets to display the correct configuration settings.
        """
        pass


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
    Window.debugMode = True                                             # TODO (AHA): What is debug mode used for?

    # Run the application
    Window.show()
    sys.exit(App.exec_())
