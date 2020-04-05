#!python3

"""
A dialog popup to display information about the application
"""

if __name__ == "__main__":
    import sys
    pkg_name = "pyqt5-template"
    pkg_dir = __file__[0:__file__.find(pkg_name)+len(pkg_name)]
    sys.path.append(pkg_dir)


# Third-party library imports
from PyQt5 import QtWidgets

# Local library imports
from modules.appdata import APPLICATION_NAME, VERSION, RELEASE_DATE
from modules.appdata import DIALOG_NAME_HELP_ABOUT


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
        layout.addWidget(QtWidgets.QLabel("Application: {}".format(APPLICATION_NAME)))
        layout.addWidget(QtWidgets.QLabel("Version: {}".format(VERSION)))
        layout.addWidget(QtWidgets.QLabel("Release Date: {}".format(RELEASE_DATE)))
        self.setLayout(layout)

    def closeEvent(self, event):
        """ Handle close event (i.e. window is closed)
        """
        pass


########################################################################
if __name__ == "__main__":

    import sys
    # Create the application
    App = QtWidgets.QApplication(sys.argv)

    # Create 'main' worker thread
    Dialog = DialogHelpAbout(None)

    # Run the application
    Dialog.show()

    sys.exit(App.exec_())
