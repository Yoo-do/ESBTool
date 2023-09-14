"""
通用窗体包,还未完成重构
"""
import json

from PyQt5.QtWidgets import QDialog, QListWidget, QBoxLayout, QDialogButtonBox, \
    QTreeWidget, QTreeWidgetItem, QStyledItemDelegate, QComboBox, QTreeView, QMessageBox, QInputDialog, QTextEdit, \
    QPushButton, QAction, QMenu, QAbstractItemView, QMainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QModelIndex, pyqtSignal

from src.utils import Data, Log


class ProjListDialog(QDialog):
    def __init__(self, parent, tittle, items):
        """
        项目弹窗列表
        """

        super().__init__(parent)

        self.setWindowTitle(tittle)

        layout = QBoxLayout(QBoxLayout.TopToBottom)

        self.list_widget = QListWidget()
        self.list_widget.addItems(items)
        layout.addWidget(self.list_widget)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        self.list_widget.doubleClicked.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

