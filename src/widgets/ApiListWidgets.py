"""
Api列表窗体
"""

from PyQt5.QtWidgets import QTreeView, QAction, QMenu, QAbstractItemView, QDialog, QInputDialog, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QDataStream, QIODevice, QModelIndex

from src.utils import FileIO, Log


class ApiListStandardItem(QStandardItem):
    def __init__(self, name: str, is_dir: bool, path: str = None):
        super().__init__(name)
        self.setEditable(False)
        self.is_dir = is_dir
        self.path = path

    def get_full_name(self):
        """
        获取模型的绝对逻辑路径
        :return:
        """
        path = []
        parent = self.parent()
        while parent is not None:
            path.insert(0, parent.text())
            parent = parent.parent()

        path.append(self.text())
        return path

    def clone(self):
        """
        复制对象
        """
        new_item = ApiListStandardItem(self.text(), self.is_dir, self.path)
        self.clone_all(new_item, self)

        return new_item

    def clone_all(self, clone_item, self_item):
        """
        递归复制对象子对象
        """
        for row in range(self_item.rowCount()):
            curr_item = self_item.child(row)
            new_item = ApiListStandardItem(curr_item.text(), curr_item.is_dir, clone_item.path)
            clone_item.appendRow(new_item)
            if curr_item.rowCount() > 0:
                self.clone_all(new_item, curr_item)


class ApiListStandardModel(QStandardItemModel):
    def __init__(self, proj_name):
        super().__init__()
        self.headers = ['接口']
        self.setHorizontalHeaderLabels(self.headers)
        self.proj_name = proj_name

    def rewrite_config(self):
        """
        回写modelConfig
        """
        config = self.generate_config(self)
        FileIO.ApiIO.rewrite_api_config(self.proj_name, config)

    def generate_config(self, parent):
        """
        递归解析模型展示树
        """
        dirs = []
        files = []

        global item

        # 获取item
        for row in range(parent.rowCount()):
            if isinstance(parent, ApiListStandardModel):
                item = parent.item(row)
            elif isinstance(parent, ApiListStandardItem):
                item = parent.child(row)

            # 获取item的属性值
            model_name = item.text()
            is_dir = item.is_dir
            path = item.path
            full_api_name = item.get_full_name()

            if is_dir:
                # 文件夹的话需要递归
                dirs.append({"name": model_name, "is_dir": is_dir, "items": self.generate_config(item)})
            else:
                # 对于修改了位置的文件进行处理 实际文件路径为逻辑路径经过md5处理
                target_path = FileIO.ApiIO.get_api_path_by_full_name(full_api_name)

                if path != target_path:
                    FileIO.ApiIO.rename_api(self.proj_name, path, target_path)

                files.append({"name": model_name, "is_dir": is_dir, "path": target_path})

        return dirs.__add__(files)


class ApiListTreeView(QTreeView):
    def __init__(self, parent, proj):
        super().__init__(parent)

        self.proj = proj

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QTreeView.ExtendedSelection)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.customContextMenuRequested.connect(self.right_clicked_menu)

