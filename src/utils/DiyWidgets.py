from PyQt5.QtWidgets import QDialog, QListWidget, QVBoxLayout, QDialogButtonBox, \
    QTreeWidget, QTreeWidgetItem, QStyledItemDelegate, QComboBox, QTreeView, QTreeWidgetItemIterator, QCheckBox
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


class DataTypeCombox(QStyledItemDelegate):
    """
    数据类型下拉框
    """

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
        tree_view.setItemDelegateForColumn(1, DataTypeCombox())

        parent.appendRow(self)
        if isinstance(parent, self.__class__):
            parent.setChild(parent.rowCount() - 1, 1, self.data_type_item)
        elif isinstance(parent, ModelStandardModel):
            parent.setItem(parent.rowCount() - 1, 1, self.data_type_item)


class ModelStandardItemNode(QStandardItem):
    """
    模型节点类
    """

    def __init__(self, tree_view: QTreeView, parent: QStandardItem, node_name, data_type,
                 is_required: bool, cn_name, description):
        super().__init__(node_name)
        self.data_type_item = QStandardItem(data_type)

        self.is_required_item = QStandardItem()
        self.is_required_item.setCheckable(True)
        self.is_required_item.setCheckState(Qt.Checked if is_required else Qt.Unchecked)

        self.cn_name_item = QStandardItem(cn_name)
        self.description_item = QStandardItem(description)

        tree_view.setItemDelegateForColumn(1, DataTypeCombox())

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

    def __json__(self):
        """
        转成对应的jsonschema
        :return:
        """
        if self.rowCount() == 1:
            root = self.item(0)
            data_type = self.item(0, 1)
            result = {"type": data_type, "properties": self.generate_json(root)}
            print(result)



    def generate_json(self, item: QStandardItem):
        result = {}
        if item.rowCount() > 0:
            for index in item.rowCount():
                child = item.child(index)
                col_name = item.child(index, 0)
                data_type = item.child(index, 1)
                require = item.child(index, 2)
                tittle = item.child(index, 3)
                description = item.child(index, 4)
                if item.child(index).rowCount() == 0:
                    result.update({col_name: {"type": data_type, "tittle": tittle, "description": description, "require": require}})
                else:
                    if data_type == 'array':
                        result.update({col_name: {"type": data_type, "items": self.generate_json(child)}})
                    elif data_type == 'object':
                        result.update({col_name: {"type": data_type, "properties": self.generate_json(child)}})
        return result

