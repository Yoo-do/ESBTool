from PyQt5.QtWidgets import QDialog, QListWidget, QVBoxLayout, QDialogButtonBox, QTreeWidget, QTreeWidgetItem


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


class ModelNodeTreeWidgetItem(QTreeWidgetItem):
    """
    模型节点展示窗体
    """
    def __init__(self, parent):
        super().__init__(parent=parent)

    def set_node_name(self, node_name):
        self.setText(0, node_name)

    def set_type_name(self, type_name):
        self.setText(0, type_name)

    def setParent(self, parent: QTreeWidget | QTreeWidgetItem):
        self.setParent(parent)










class ModelNodeTreeWidget(QTreeWidget):
    """
    模型展示窗体
    """
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setColumnCount(2)
        self.headers = ["节点", "类型", '中文名', '说明']
        self.setHeaderLabels(self.headers)



