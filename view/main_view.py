from PyQt5 import QtWidgets

from view.main_window import Ui_MainWindow
from view.forms.input_form_sidebar import Ui_input_form_sidebar as InputFormSidebar

class MainView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PASK')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


    def display_message(self, text, duration=3000):
        self.ui.statusbar.showMessage(text, duration)
