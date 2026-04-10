from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from typing_extensions import override


class GenericTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data_list, headers):
        super().__init__()
        self._data = data_list
        self._headers = headers

    @override
    def rowCount(self, parent = None):
        return len(self._data)

    @override
    def columnCount(self, parent = None):
        return len(self._headers)

    @override
    def data(self, index, role=Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            obj = self._data[index.row()]
            attr_name = self._headers[index.column()]
            return str(getattr(obj, attr_name, ""))
        return None

    @override
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self._headers[section]
        return None