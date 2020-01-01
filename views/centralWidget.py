#!python3
#!/usr/bin/python
# -*- coding: utf-8 -*-

""" CentralWidget example

Last Updated: 18 December 2019 (Ali Al-Hakim)
"""

# Standard Library Imports
import os
import logging
debugLogger = logging.getLogger(__name__)

# Third-Party Library Imports
from PyQt5 import QtCore, QtGui, QtWidgets


########################################################################
# Choose whether to display the Test Button or not
VIEW_TEST_MODE = False

# Import Stylesheet Contents
with open(os.path.join(os.path.dirname(__file__), "styles.css"), "r") as rf:
    STYLESHEET = rf.read()

########################################################################
# Valid QtWidgets.QLabel stylesheet background colours
# Tree widget RGB colour options
BLACK  = (  0,   0,   0)
RED    = (250,  40,  40)
GREEN  = ( 60, 220,  60)
AMBER  = (250, 250, 110)
PURPLE = (220, 120, 220)
BLUE   = ( 60, 170, 240)
ORANGE = (240, 140,  60)
YELLOW = (250, 210, 110)

def rgb_to_hex(rgb):
    hex_r = str(hex(rgb[0]).replace("0x", ""))
    hex_g = str(hex(rgb[1]).replace("0x", ""))
    hex_b = str(hex(rgb[2]).replace("0x", ""))
    return "#" + hex_r + hex_g + hex_b


########################################################################
class CentralWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(CentralWidget, self).__init__(parent=parent)

        # Create links to important parent properties, for convenience
        self.setStyleSheet(STYLESHEET)
        self.parent = parent

        # Draw UI
        self.slots = {}
        for slot_id in range(6):
            label = QtWidgets.QLabel("", self)
            label.setFixedWidth(300)
            label.setFixedHeight(300)
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.slots[slot_id] = label

        testSlotLayout = QtWidgets.QGridLayout()
        for slot_id in self.slots:
            self.waiting(slot_id)

            if slot_id % 2 == 0:    # Even numbers
                row = 0
                column = int(slot_id / 2)
            else:                   # Odd numbers
                row = 1
                column = int((slot_id / 2.0) - 0.5)

            widget = self.slots[slot_id]
            testSlotLayout.addWidget(widget, row, column)

        principalLayout = QtWidgets.QVBoxLayout()
        principalLayout.addLayout(testSlotLayout)

        # Show a button to test the change colour/text functions
        if VIEW_TEST_MODE:
            buttonLayout = QtWidgets.QHBoxLayout()
            ybutton = QtWidgets.QPushButton("WAIT")
            obutton = QtWidgets.QPushButton("TEST")
            gbutton = QtWidgets.QPushButton("PASS")
            rbutton = QtWidgets.QPushButton("FAIL")
            ybutton.clicked.connect(self.test_yellow)
            obutton.clicked.connect(self.test_orange)
            gbutton.clicked.connect(self.test_green)
            rbutton.clicked.connect(self.test_red)
            buttonLayout.addWidget(ybutton)
            buttonLayout.addWidget(obutton)
            buttonLayout.addWidget(gbutton)
            buttonLayout.addWidget(rbutton)
            principalLayout.addLayout(buttonLayout)

        self.setLayout(principalLayout)

    def _validate_slot(self, slot_id):
        """ Make sure the slot_id is in the correct range

        Args:
            slot_id: Integer representation of the test slot

        Returns:
            Nothing.

        Raises:
            RuntimeError: This method will attempt to crash the program
                if the slot_id cannot be validated as this will result
                in the application not displaying information correctly.
        """
        if slot_id < 0 or slot_id > 5:
            raise(RuntimeError, "Invalid SLOT_ID. Must be 1-6, not '{}'".format(slot_id))

    def change_colour(self, slot_id, colour):
        """ Update the colour of the test slot visualisation

        Args:
            slot_id: Integer representation of the test slot
            colour: This should be a program defined colour i.e.
                    RED, YELLOW, GREEN.

        Returns:
            Nothing. This method will just change the background colour
            of the frame associated with `slot_id`.
        """
        self.slots[slot_id].setStyleSheet("background-color:{}".format(colour))

    def change_text(self, slot_id, text):
        """ Update the text in the test slot visualisation

        Args:
            slot_id: Integer representation of the test slot
            text: String object containing information to display in the
                  test slot frame.

        Returns:
            Nothing. This method will just change the text displayed in
            the GUI frame associated with `slot_id`.
        """
        self.slots[slot_id].setText(text)

    #------------------------------------------------------------------#
    # Slots
    QtCore.pyqtSlot(int, str)
    def failed(self, slot_id, text=""):
        self._validate_slot(slot_id)
        self.change_colour(slot_id, rgb_to_hex(RED))
        self.change_text(slot_id, "BON {}\n\nFAIL\n{}".format(slot_id+1, text))

    QtCore.pyqtSlot(int, str)
    def passed(self, slot_id, text=""):
        self._validate_slot(slot_id)
        self.change_colour(slot_id, rgb_to_hex(GREEN))
        self.change_text(slot_id, "BON {}\n\nPASS\n{}".format(slot_id+1, text))

    QtCore.pyqtSlot(int, str)
    def testing(self, slot_id, text=""):
        self._validate_slot(slot_id)
        self.change_colour(slot_id, rgb_to_hex(ORANGE))
        self.change_text(slot_id, "BON {}\n\nTESTING\n{}".format(slot_id+1, text))

    QtCore.pyqtSlot(int)
    def waiting(self, slot_id):
        self._validate_slot(slot_id)
        self.change_colour(slot_id, rgb_to_hex(YELLOW))
        self.change_text(slot_id, "BON {}\n\nInsert Device\n".format(slot_id+1))

    #------------------------------------------------------------------#
    # Test Methods
    def test_yellow(self):
        for slot_id in self.slots:
            self.waiting(slot_id)

    def test_orange(self):
        for slot_id in self.slots:
            self.testing(slot_id, "In Progress")

    def test_green(self):
        for slot_id in self.slots:
            self.passed(slot_id, "ID #2764{}54".format(slot_id))

    def test_red(self):
        for slot_id in self.slots:
            self.failed(slot_id, "E01: Something bad")


########################################################################
if __name__ == "__main__":

    from mainWindow import MainWindow
    import sys

    # Create the application.
    App = QtWidgets.QApplication(sys.argv)

    # Create "main" worker threads.
    Window = MainWindow()
    Window.debugMode = True

    # Add the application 'central widget' to the window object.
    Window.setMainWidget(CentralWidget(Window))

    # Run the application.
    Window.show()
    sys.exit(App.exec_())
