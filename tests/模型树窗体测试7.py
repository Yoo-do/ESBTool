from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QTreeView, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem




class ModelStandardModel(QStandardItemModel):
    def __init__(self):
        super().__init__()
        self.headers = ['名称']
        self.setHorizontalHeaderLabels(self.headers)


class ModelStandardItem(QStandardItem):
    def __init__(self, name: str, is_dir: bool, path: str):
        super().__init__(name)
        self.is_dir = is_dir
        self.path = path

    def clone(self):
        new_item = ModelStandardItem(self.text(), self.is_dir, self.path)
        self.clone_all(new_item, self)

        return new_item


    def clone_all(self, clone_item, self_item):
        for row in range(self_item.rowCount()):
            curr_item = self_item.child(row)
            new_item = ModelStandardItem(curr_item.text(), curr_item.is_dir, clone_item.path)
            clone_item.appendRow(new_item)
            if curr_item.rowCount() > 0:
                self.clone_all(new_item, curr_item)





class ModelTreeView(QTreeView):
    def __init__(self):
        super().__init__()
        self.show()

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QTreeView.ExtendedSelection)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.clicked.connect(self.click_event)

    def click_event(self):
        index = self.currentIndex()
        item = self.model().itemFromIndex(index)

        print(f'name:{item.text()}, path:{item.path}')

    def dropEvent(self, event):
        # 获取拖放操作的源节点
        source_index = event.source().currentIndex()
        source_item = self.model().itemFromIndex(source_index)

        drop_position = self.dropIndicatorPosition()
        target_index = self.indexAt(event.pos())
        target_item = self.model().itemFromIndex(target_index)

        # 放置节点的限制 重构创建和删除方法后就无法调用父级dropEvent方法，只能自己枚举重构
        if drop_position == QAbstractItemView.OnItem:
            if target_item.is_dir is False:
                # 不允许放在model节点内
                event.ignore()
                return
            else:
                if target_item is not None:
                    target_item.appendRow(source_item.clone())
                else:
                    self.model().appendRow(source_item.clone())

        elif drop_position == QAbstractItemView.AboveItem:
            """拖拽到上方时"""
            print('拖拽到上方')
            parent = target_item.parent()
            if parent is None:
                parent = self.model()

            parent.insertRow(target_index.row(), source_item.clone())

        elif drop_position == QAbstractItemView.BelowItem:
            """拖拽到下方时"""
            print('拖拽到下方')
            parent = target_item.parent()
            if parent is None:
                parent = self.model()

            parent.insertRow(target_index.row() + 1, source_item.clone())

        elif drop_position == QAbstractItemView.OnViewport:
            """拖拽到空白处"""
            self.model().insertRow(self.model().rowCount(), source_item.clone())


        # 移除原结点
        if source_item.parent() is not None:
            source_item.parent().removeRow(source_item.row())
        else:
            self.model().removeRow(source_item.row())

        event.accept()


    def add_child_node(self, index, node=None):
        pass

    def add_pre_node(self, index, node=None):
        pass

    def add_post_node(self, index, node=None):
        pass


if __name__ == '__main__':
    app = QApplication([])

    model = ModelStandardModel()
    treeView = ModelTreeView()


    # 生成结点

    root1 = ModelStandardItem('文件夹1', True, '')
    root1.appendRow(ModelStandardItem('结点1', False, '文件夹1路径1'))
    root1.appendRow(ModelStandardItem('结点2', False, '文件夹1路径2'))
    root1.appendRow(ModelStandardItem('结点3', False, '文件夹1路径3'))
    model.appendRow(root1)

    root2 = ModelStandardItem('文件夹2', True, '')
    root2.appendRow(ModelStandardItem('结点1', False, '文件夹2路径1'))
    root2.appendRow(ModelStandardItem('结点2', False, '文件夹2路径2'))
    model.appendRow(root2)

    treeView.setModel(model)



    treeView.setModel(model)




    treeView.setModel(model)


    treeView.show()
    app.exec()
