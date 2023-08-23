from PyQt5.QtWidgets import QApplication, QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

if __name__ == '__main__':
    app = QApplication([])

    # 创建一个QStandardItemModel对象
    model = QStandardItemModel()

    # 创建一些QStandardItem对象，并将其添加到模型中
    item1 = QStandardItem('Item 1')
    item2 = QStandardItem('Item 2')
    item3 = QStandardItem('Item 3')
    model.appendRow([item1, item2, item3])

    # 创建一个QTreeView对象，并将模型设置为其数据源
    tree_view = QTreeView()
    tree_view.setModel(model)

    # 允许编辑
    tree_view.setEditTriggers(QTreeView.AllEditTriggers)

    # 显示窗口
    tree_view.show()

    app.exec_()