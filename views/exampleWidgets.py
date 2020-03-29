#!python3
#!/usr/bin/python
# -*- coding: utf-8 -*-

""" CentralWidget example

You must have PyQt5 installed to run this code:
 - Windows: python3 -m pip install pyqt5
 - Unix: sudo apt install python3-pyqt5

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

        #---------------------------------------------------------------
        # Example of a QLabel
        label_title = self.createLabel("QLabel")
        label_example = self.createLabel("This is an example label")

        labelLayout = QtWidgets.QVBoxLayout()
        labelLayout.addWidget(label_title)
        labelLayout.addWidget(label_example)

        #---------------------------------------------------------------
        # Example of a QPushButton
        button_title = self.createLabel("QPushButton")
        button_example = self.createPushButton("Push Me", self.pushButtonAction, height=40)

        pushButtonLayout = QtWidgets.QVBoxLayout()
        pushButtonLayout.addWidget(button_title)
        pushButtonLayout.addWidget(button_example)

        #---------------------------------------------------------------
        # Example of a QLineEdit
        lineEdit_title = self.createLabel("QLineEdit")
        lineEdit_example = self.createLineEdit(text="Type something here",
            height=40, enabled=False, readonly=True)

        lineEditLayout = QtWidgets.QVBoxLayout()
        lineEditLayout.addWidget(lineEdit_title)
        lineEditLayout.addWidget(lineEdit_example)

        #---------------------------------------------------------------
        # Example of a QDateTimeEdit
        datetimeSelector_title = self.createLabel("QDateTimeEdit")
        datetimeSelector_example = self.createDatetimeSelector(show_calendar=True,
            format="dd-MM-yyyy", date="29-03-2020", command=self.dateChangedAction)

        datetimeSelectorLayout = QtWidgets.QVBoxLayout()
        datetimeSelectorLayout.addWidget(datetimeSelector_title)
        datetimeSelectorLayout.addWidget(datetimeSelector_example)

        #---------------------------------------------------------------
        # Example of a custom FilteredDropdown widget
        example_list = ["Homer Simpson", "Marge Simpson", "Lisa Simpson", "Bart Simpson", "Maggie Simpson"]
        dropdown_title = self.createLabel("Dropdown (QComboBox)")
        dropdown_example = self.createDropdown(example_list)

        dropdownLayout = QtWidgets.QVBoxLayout()
        dropdownLayout.addWidget(dropdown_title)
        dropdownLayout.addWidget(dropdown_example)

        #---------------------------------------------------------------
        # Example of a custom FilteredDropdown widget
        filteredDropdown_title = self.createLabel("FilteredDropdown (custom widget)")
        filteredDropdown_example = self.createFilteredDropdown(example_list, height=30)

        filteredDropdownLayout = QtWidgets.QVBoxLayout()
        filteredDropdownLayout.addWidget(filteredDropdown_title)
        filteredDropdownLayout.addWidget(filteredDropdown_example)

        #---------------------------------------------------------------
        # Define a layout for the widgets
        principalLayout = QtWidgets.QVBoxLayout()
        principalLayout.addLayout(labelLayout)
        principalLayout.addLayout(pushButtonLayout)
        principalLayout.addLayout(lineEditLayout)
        principalLayout.addLayout(datetimeSelectorLayout)
        principalLayout.addLayout(dropdownLayout)
        principalLayout.addLayout(filteredDropdownLayout)
        self.setLayout(principalLayout)

    def pushButtonAction(self):
        """ Do something when the push button is pressed. """
        print("You pressed the push button")

    def dateChangedAction(self, new_date):
        """ Do something when the date selector date is changed. """
        print("The date was changed to {}".format(QtCore.QDate.toString(new_date)))


    #-------------------------------------------------------------------
    def createLabel(self, text, **kwargs):
        """ Create a QLabel object.

        [Args]
        text: What to display in the label.
        kwargs:
            height <int>: in pixels
            width <int>: in pixels
        """
        label = QtWidgets.QLabel(text, parent=self.parent)

        if "width" in kwargs:
            label.setFixedWidth(kwargs["width"])
        if "height" in kwargs:
            label.setFixedHeight(kwargs["height"])

        return label

    def createLineEdit(self, **kwargs):
        """
        Create a line edit field.

        [Args]
        kwargs:
            height <int>: in pixels
            width <int>: in pixels
            enabled <boolean>: choose if the text can be selected
            readonly <boolean>: choose if the text can be edited
            text <str>: A string to display
        """
        lineEdit = QtWidgets.QLineEdit(self)

        if "width" in kwargs:
            lineEdit.setFixedWidth(kwargs["width"])
        if "height" in kwargs:
            lineEdit.setFixedHeight(kwargs["height"])
        if "enabled" in kwargs:
            lineEdit.setEnabled(kwargs["enabled"])
        if "readonly" in kwargs:
            lineEdit.setReadOnly(kwargs["readonly"])
        if "text" in kwargs:
            lineEdit.setText(kwargs["text"])

        return lineEdit

    def createPushButton(self, text, command, **kwargs):
        """
        Create a push button with name and linked action.

        [Args]
        label: text written on the button.
        command: The function to be called when the button is pressed.
        kwargs:
            height <int>: in pixels
            width <int>: in pixels
        """
        button = QtWidgets.QPushButton(text, parent=self.parent)
        button.clicked.connect(command)

        if "width" in kwargs:
            button.setFixedWidth(kwargs["width"])
        if "height" in kwargs:
            button.setFixedHeight(kwargs["height"])

        return button


    def createDatetimeSelector(self, **kwargs):
        """
        Create a date and time selector widget.

        [Args]
        kwargs:
            height <int>: in pixels
            width <int>: in pixels
            datetime <str>: e.g. "29-03-2020"
            format <str>: e.g. "dd-MM-yyyy"
            show_calendar <boolean>: to show a calendar selector
            command <method>: a command to call if the date is changed
        """
        datetimeSelector = QtWidgets.QDateTimeEdit(self)

        if "width" in kwargs:
            datetimeSelector.setFixedWidth(kwargs["width"])
        if "height" in kwargs:
            datetimeSelector.setFixedHeight(kwargs["height"])
        if "format" in kwargs:
            if "datetime" in kwargs:
                qdatetime = QtCore.QDate.fromString(kwargs["height"], kwargs["format"])
            else:
                qdatetime = QtCore.QDate.currentDate().addDays(-1)
            datetimeSelector.setDisplayFormat(kwargs["format"])
            datetimeSelector.setDate(qdatetime)

        if "show_calendar" in kwargs:
            datetimeSelector.setCalendarPopup(kwargs["show_calendar"])
        if "command" in kwargs:
            datetimeSelector.dateChanged.connect(kwargs["command"])

        return datetimeSelector

    def createDropdown(self, options, **kwargs):
        """
        Create a drop-down list.

        [Args]
        options: A list of terms to display in the dropdown menu.
        kwargs:
            height <int>: in pixels
            width <int>: in pixels
            enabled <boolean>: choose if the field can be used or not
            editable <boolean>: choose if the text can be edited
        """
        # Create a drop-down field to display the entity list
        dropdown = QtWidgets.QComboBox(self)
        dropdown.setFixedHeight(30)
        dropdown.setEditable(False)
        for option in options:
            dropdown.addItem(option)

        if "width" in kwargs:
            dropdown.setFixedWidth(kwargs["width"])
        if "height" in kwargs:
            dropdown.setFixedHeight(kwargs["height"])
        if "enabled" in kwargs:
            dropdown.setEnabled(kwargs["enabled"])
        if "editable" in kwargs:
            dropdown.setEditable(kwargs["editable"])

        return dropdown

    def createFilteredDropdown(self, options, **kwargs):
        """
        Create a drop-down list with a search-filter feature

        [Args]
        options: A list of terms to display in the dropdown menu.
        kwargs:
            height <int>: in pixels
        """
        dropdown = FilteredDropdown(self, options, **kwargs)

        return dropdown


class FilteredDropdown(QtWidgets.QWidget):
    """
    Create a drop-down list with a search-filter feature

    [Args]
    parent: A parent QObject.
    options: A list of terms to display in the dropdown menu.
    kwargs:
        height <int>: in pixels
    """
    def __init__(self, parent, options, **kwargs):
        super(FilteredDropdown, self).__init__(parent=parent)
        self.parent = parent
        self.options = options

        # Create a text filter bar
        self.text = QtWidgets.QLineEdit(self)
        self.text.setMaximumWidth(200)
        self.text.returnPressed.connect(self._update_list)
        self.text.textEdited.connect(self._update_list)

       # Create a drop-down field to display the entity list
        self.list = QtWidgets.QComboBox(self)
        self.list.setEditable(False)
        for option in options:
            self.list.addItem(option)

        # if "width" in kwargs:
        #     self.text.setFixedWidth(kwargs["width"]*(1/4))
        #     self.list.setFixedWidth(kwargs["width"]*(3/4))
        if "height" in kwargs:
            self.text.setFixedHeight(kwargs["height"])
            self.list.setFixedHeight(kwargs["height"])

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.list)

        self.setLayout(layout)

    def _update_list(self):
        """ Filter the options displayed in self.dropdown
        """
        # Clear the drop-down list
        self.list.clear()

        # Obtain search term
        search_term = str(self.text.text()).upper().strip(" ")

        # Filter the entity list based off keywords
        display_options = []
        if self.options == []:
            display_options = [" -- Empty -- "]

        elif search_term == "":
            display_options += self.options

        else:
            for option in self.options:
                if search_term.upper() in option.upper():
                    display_options.append(option)

        for option in display_options:
            self.list.addItem(option)

    def selected(self):
        """ Return the item selected from the dropdown list.
        """
        return str(self.list.currentText())


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
