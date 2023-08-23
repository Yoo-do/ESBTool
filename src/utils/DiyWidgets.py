from PyQt5.QtWidgets import QDialog, QListWidget, QVBoxLayout, QDialogButtonBox, \
    QTreeWidget, QTreeWidgetItem, QStyledItemDelegate, QComboBox, QTreeView, QTreeWidgetItemIterator
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

from src.utils import Data


class ListDialog(QDialog):
    def __init__(self, parent, tittle, items):
        """
        弹窗列表
        """

        super().__init__(parent)

        self.show()
        self.setWindowTitle(tittle)

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.addItems(items)
        layout.addWidget(self.list_widget)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)


class ComboBoxDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.addItems(Data.ModelDataTypes)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, role=Qt.DisplayRole)
        editor.setCurrentText(value)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, role=Qt.EditRole)


class ModelTreeView(QTreeView):
    """
    模型展示窗体
    """

    def __init__(self, parent):
        super().__init__(parent=parent)


class ModelStandardItemDir(QStandardItem):
    """
    模型文件类
    """

    def __init__(self, tree_view: QTreeView, parent: QStandardItem | QStandardItemModel, dir_name, data_type):
        super().__init__(dir_name)
        self.data_type_item = QStandardItem(data_type)
        tree_view.setItemDelegateForColumn(1, ComboBoxDelegate())

        parent.appendRow(self)
        if isinstance(parent, self.__class__):
            parent.setChild(parent.rowCount() - 1, 1, self.data_type_item)
        elif isinstance(parent, ModelStandardModel):
            parent.setItem(parent.rowCount() - 1, 1, self.data_type_item)


class ModelStandardItemNode(QStandardItem):
    """
    模型节点类
    """

    def __init__(self, tree_view: QTreeView, parent: QStandardItem | QStandardItemModel, node_name, data_type,
                 is_required, cn_name, description):
        super().__init__(node_name)
        self.data_type_item = QStandardItem(data_type)
        self.is_required_item = QStandardItem(is_required)
        self.cn_name_item = QStandardItem(cn_name)
        self.description_item = QStandardItem(description)
        tree_view.setItemDelegateForColumn(1, ComboBoxDelegate())

        parent.appendRow(self)
        parent.setChild(parent.rowCount() - 1, 1, self.data_type_item)
        parent.setChild(parent.rowCount() - 1, 2, self.is_required_item)
        parent.setChild(parent.rowCount() - 1, 3, self.cn_name_item)
        parent.setChild(parent.rowCount() - 1, 4, self.description_item)


class ModelStandardModel(QStandardItemModel):
    def __init__(self):
        super().__init__()
        self.headers = ['节点', '类型', '必选', '中文名', '描述']
        self.setHorizontalHeaderLabels(self.headers)
