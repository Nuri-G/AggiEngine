from PySide2.QtCore import QMetaObject
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow


class UiManager(QUiLoader):

    def __init__(self, window, customWidgets=None):
        QUiLoader.__init__(self)
        self.window = window

        # Register all the custom widgets so that they can be created later
        self.customWidgets = customWidgets
        if customWidgets is not None:
            for wid in customWidgets:
                self.registerCustomWidget(wid)

    def createWidget(self, class_name, parent=None, name=''):
        """
        Overrides QUiLoader to createWidget in current window rather than a new one
        :param class_name: The class we want to create
        :param parent: The parent widget
        :param name: The name of the widget we'll create
        :return: The created widget
        """

        if class_name is QMainWindow:
            return self.window

        if parent is None and self.window:
            return self.window
        else:
            if class_name in self.availableWidgets():
                widget = QUiLoader.createWidget(self, class_name, parent, name)
                widget.show()
            else:
                try:
                    widget = self.customWidgets[class_name](parent)
                except (TypeError, KeyError) as e:
                    raise Exception(class_name, 'was not found are you sure it was promoted?')

            if self.window:
                setattr(self.window, name, widget)

            return widget

    def loadWidgets(self, ui_file, deleteCurrent=False):
        """
        Loads the current ui_file and if wanted deleted old widgets
        :param ui_file: The file path to load
        :param deleteCurrent: Remove old widgets
        :return: None
        """
        if len(self.window.children()) > 0 and deleteCurrent:
            for i in reversed(range(3, len(self.window.children()))):
                self.window.children()[i].deleteLater()

        widgets = self.load(ui_file)  # load widgets
        QMetaObject.connectSlotsByName(widgets)
