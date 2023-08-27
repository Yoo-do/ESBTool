from PyQt5.QtWidgets import QApplication, QTreeView, QMenu, QAction, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class TreeView(QTreeView):
    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, pos):
        index = self.indexAt(pos)
        if index.isValid():
            menu = QMenu(self)
            if self.model().hasChildren(index):
                add_action = QAction("新增子节点", self)
                add_action.triggered.connect(self.addChildNode)
                menu.addAction(add_action)
            else:
                insert_before_action = QAction("在前方插入新节点", self)
                insert_before_action.triggered.connect(self.insertBeforeNode)
                insert_after_action = QAction("在后方插入新节点", self)
                insert_after_action.triggered.connect(self.insertAfterNode)
                menu.addAction(insert_before_action)
                menu.addAction(insert_after_action)
            delete_action = QAction("删除节点", self)
            delete_action.triggered.connect(self.deleteNode)
            menu.addAction(delete_action)
            menu.exec_(self.viewport().mapToGlobal(pos))

    def deleteNode(self):
        index = self.currentIndex()
        if index.isValid():
            self.model().removeRow(index.row(), index.parent())

    def addChildNode(self):
        index = self.currentIndex()
        if index.isValid():
            self.model().insertRow(self.model().rowCount(index), index)
            child_index = self.model().index(self.model().rowCount(index) - 1, 0, index)
            self.setCurrentIndex(child_index)
            self.edit(child_index)

    def insertBeforeNode(self):
        index = self.currentIndex()
        if index.isValid():
            parent = index.parent()
            row = index.row()
            self.model().insertRow(row, parent)
            new_index = self.model().index(row, 0, parent)
            self.setCurrentIndex(new_index)
            self.edit(new_index)

    def insertAfterNode(self):
        index = self.currentIndex()
        if index.isValid():
            parent = index.parent()
            row = index.row() + 1
            self.model().insertRow(row, parent)
            new_index = self.model().index(row, 0, parent)
            self.setCurrentIndex(new_index)
            self.edit(new_index)


def get_model(parent):
    model = QStandardItemModel(parent)
    model.setHorizontalHeaderLabels(['项目名称', '信息'])

    itemProject = QStandardItem('项目')
    model.appendRow(itemProject)
    model.setItem(0, 1, QStandardItem('项目信息说明'))

    itemChild = QStandardItem('文件夹1')
    itemProject.appendRow(itemChild)
    itemProject.setChild(0, 1, QStandardItem('信息说明'))

    itemFolder = QStandardItem('文件夹2')
    itemProject.appendRow(itemFolder)
    for group in range(5):
        itemGroup = QStandardItem('组{}'.format(group + 1))
        itemFolder.appendRow(itemGroup)
        for ch in range(group + 1):
            itemCh = QStandardItem('成员{}'.format(ch + 1))
            itemCh.setCheckable(True)
            itemGroup.appendRow(itemCh)
            itemGroup.setChild(itemCh.index().row(), 1, QStandardItem('成员{}信息说明'.format(ch + 1)))
    itemProject.setChild(itemFolder.index().row(), 1, QStandardItem('文件夹2信息说明'))

    return model

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tree_view = TreeView()
    tree_view.setModel(get_model(tree_view))
    tree_view.show()
    sys.exit(app.exec_())