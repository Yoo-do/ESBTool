from PyQt5.QtWidgets import QApplication, QTreeView, QMenu, QAction, QMessageBox
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
            delete_action = QAction("删除节点", self)
            add_action = QAction("新增节点", self)
            delete_action.triggered.connect(self.deleteNode)
            add_action.triggered.connect(self.addNode)
            menu.addAction(delete_action)
            menu.addAction(add_action)
            menu.exec_(self.viewport().mapToGlobal(pos))

    def deleteNode(self):
        index = self.currentIndex()
        if index.isValid():
            # 执行删除节点的操作
            self.model().removeRow(index.row(), index.parent())

    def addNode(self):
        index = self.currentIndex()
        if index.isValid():
            # 执行新增节点的操作
            self.model().insertRow(index.row()+1, index.parent())


def get_model(parent):
    model = QStandardItemModel(parent)
    model.setHorizontalHeaderLabels(['项目名称', '信息'])

    # 添加条目
    itemProject = QStandardItem('项目')
    model.appendRow(itemProject)
    model.setItem(0, 1, QStandardItem('项目信息说明'))

    # 添加子条目
    itemChild = QStandardItem('文件夹1')
    itemProject.appendRow(itemChild)
    itemProject.setChild(0, 1, QStandardItem('信息说明'))

    # 继续添加
    itemFolder = QStandardItem('文件夹2')
    itemProject.appendRow(itemFolder)
    for group in range(5):
        itemGroup = QStandardItem('组{}'.format(group + 1))
        itemFolder.appendRow(itemGroup)
        for ch in range(group + 1):
            itemCh = QStandardItem('成员{}'.format(ch + 1))
            # 添加复选框
            itemCh.setCheckable(True)
            itemGroup.appendRow(itemCh)
            itemGroup.setChild(itemCh.index().row(), 1, QStandardItem('成员{}信息说明'.format(ch + 1)))
    itemProject.setChild(itemFolder.index().row(), 1, QStandardItem('文件夹2信息说明'))

    return model

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tree_view = TreeView()
    # 设置你的树形视图的模型
    tree_view.setModel(get_model(tree_view))
    tree_view.show()
    sys.exit(app.exec_())