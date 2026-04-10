import sys
from PyQt5 import QtWidgets

from view.main_view import MainView
from controller.main_controller import MainController
from tests.test import populateDB
from model.db import buildDB

if __name__ == "__main__":
    #buildDB.build()

    app = QtWidgets.QApplication(sys.argv)

    view = MainView()
    controller = MainController(view)

    view.show()
    sys.exit(app.exec_())