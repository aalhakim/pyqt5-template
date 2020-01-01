#!python3
#!/usr/bin/python
# -*- coding: utf-8 -*-

""" CentralWidget example

Last Updated: 18 December 2019 (Ali Al-Hakim)
"""

# Standard Library Imports
import logging
debugLogger = logging.getLogger(__name__)

# Third-Party Library Imports
from PyQt5 import QtCore, QtGui, QtWidgets


########################################################################
class exampleWidgets(QtWidgets.QWidget):
    """
    A central widget container for other widget types
    """

    def __init__(self, parent):
        super(exampleWidgets, self).__init__(parent=parent)
        self.parent = parent

        # Example of a QLabel
        label_title = self.createLabel("QLabel")
        label_example = self.createLabel("This is an example label")

        labelLayout = QtWidgets.QVBoxLayout()
        labelLayout.addWidget(label_title)
        labelLayout.addWidget(label_example)

        # Example of a QPushButton
        button_title = self.createLabel("QPushButton")
        button_example = self.createPushButton("Push Me", self.pushButtonAction, height=40)

        pushButtonLayout = QtWidgets.QVBoxLayout()
        pushButtonLayout.addWidget(button_title)
        pushButtonLayout.addWidget(button_example)

        # Define a layout for the widgets
        principalLayout = QtWidgets.QVBoxLayout()
        principalLayout.addLayout(labelLayout)
        principalLayout.addLayout(pushButtonLayout)
        self.setLayout(principalLayout)

    def pushButtonAction(self):
        """ Do something when the push button is pressed. """
        print("You pressed the push button")


    #-------------------------------------------------------------------
    def createLabel(self, text, **kwargs):
        """ Create a QLabel object.

        [Args]
        text: What to display in the label.
        """
        label = QtWidgets.QLabel(text, parent=self.parent)

        if "width" in kwargs:
            label.setFixedWidth(kwargs["width"])
        if "height" in kwargs:
            label.setFixedHeight(kwargs["height"])

        return(label)


    def createPushButton(self, text, command, **kwargs):
        """
        Create a push button with name and linked action.

        [Args]
        label: text written on the button
        command: The function to be called when the button is pressed
        """
        button = QtWidgets.QPushButton(text, parent=self.parent)
        button.clicked.connect(command)

        if "width" in kwargs:
            button.setFixedWidth(kwargs["width"])
        if "height" in kwargs:
            button.setFixedHeight(kwargs["height"])

        return(button)



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
    Window.setMainWidget(exampleWidgets(Window))

    # Run the application.
    Window.show()
    sys.exit(App.exec_())
