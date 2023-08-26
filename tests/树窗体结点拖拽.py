from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QMenu, QAction, QAbstractItemView
from PyQt5.QtCore import Qt, QMimeData, QByteArray, QDataStream, QIODevice
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class MyTreeModel(QStandardItemModel):
    def __init__(self):
        super().__init__()

        # 添加根节点
        root_item = QStandardItem("根节点")
        self.appendRow(root_item)

        # 添加子节点
        child_item1 = QStandardItem("子节点1")
        child_item2 = QStandardItem("子节点2")
        root_item.appendRow(child_item1)
        root_item.appendRow(child_item2)

        # 添加孙子节点
        grandchild_item1 = QStandardItem("孙子节点1")
        grandchild_item2 = QStandardItem("孙子节点2")
        child_item1.appendRow(grandchild_item1)
        child_item1.appendRow(grandchild_item2)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tree_view = QTreeView(self)
        self.tree_view.setDragEnabled(True)
        self.tree_view.setAcceptDrops(True)
        self.tree_view.setDropIndicatorShown(True)
        self.tree_view.setDragDropMode(QAbstractItemView.InternalMove)
        self.tree_view.setDefaultDropAction(Qt.MoveAction)
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.create_menu)
        self.setCentralWidget(self.tree_view)

        self.model = MyTreeModel()
        self.tree_view.setModel(self.model)

    def create_menu(self, position):
        index = self.tree_view.indexAt(position)
        if index.isValid():
            menu = QMenu()
            add_action = QAction("新增节点", menu)
            delete_action = QAction("删除节点", menu)
            add_action.triggered.connect(lambda: self.add_node(index))
            delete_action.triggered.connect(lambda: self.delete_node(index))
            menu.addAction(add_action)
            menu.addAction(delete_action)
            menu.exec_(self.tree_view.viewport().mapToGlobal(position))

    def add_node(self, parent_index):
        parent_item = self.model.itemFromIndex(parent_index)
        new_item = QStandardItem("新节点")
        parent_item.appendRow(new_item)

    def delete_node(self, index):
        item = self.model.itemFromIndex(index)
        parent_item = item.parent()
        if parent_item is None:
            return
        row = item.row()
        parent_item.removeRow(row)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            index = self.tree_view.indexAt(event.pos())
            item = self.model.itemFromIndex(index)
            if item.text() == "特定值":
                event.ignore()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()
    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            data = event.mimeData().data("application/x-qabstractitemmodeldatalist")
            stream = QDataStream(data, QIODevice.ReadOnly)

            target_index = self.tree_view.indexAt(event.pos())
            target_parent = target_index.parent()

            if target_index.isValid() and target_parent.isValid():
                row = target_index.row()
                column = target_index.column()

                self.model.dropMimeData(data, Qt.MoveAction, row, column, target_parent)

            event.acceptProposedAction()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()