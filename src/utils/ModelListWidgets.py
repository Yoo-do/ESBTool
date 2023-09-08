from PyQt5.QtWidgets import QTreeView, QAction, QMenu, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QDataStream, QIODevice
import hashlib

from src.utils import FileIO, Log


class ModelListStandardItem(QStandardItem):
    def __init__(self, parent: QStandardItemModel | QStandardItem, name: str, is_dir: bool, path: str = None):
        super().__init__(name)
        self.is_dir = is_dir
        self.path = path
        parent.appendRow([self])

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




class ModelListStandardModel(QStandardItemModel):
    def __init__(self, proj_name):
        super().__init__()
        self.headers = ['名称']
        self.setHorizontalHeaderLabels(self.headers)
        self.proj_name = proj_name

    def rewrite_config(self):
        config_data = self.generate_config()
        FileIO.ProjIO.rewrite_model_config(self.proj_name, config_data)

    def generate_config(self):
        """
        生成modelConfig数据
        :return:
        """
        # 完成文件夹排序后返回
        config = self.generate_json(self)
        return config

    def generate_json(self, parent: ModelListStandardItem):
        dirs = []
        files = []

        for row in range(parent.rowCount()):
            item = None
            if isinstance(parent, ModelListStandardModel):
                item = parent.item(row)
            elif isinstance(parent, ModelListStandardItem):
                item = parent.child(row)

            if item.is_dir:
                dirs.append({"name": item.text(), "is_dir": item.is_dir, "items": self.generate_json(item)})
            else:
                # 对于修改了位置的文件进行处理 实际文件路径为逻辑路径经过md5处理
                target_path = hashlib.md5(item.get_full_name().__str__().encode()).hexdigest()

                if item.path != target_path:
                    FileIO.ProjIO.rename_model(self.proj_name, item.path, target_path)

                files.append({"name": item.text(), "is_dir": item.is_dir, "path": target_path})

        return dirs.__add__(files)

class ModelListTreeView(QTreeView):
    def __init__(self, parent, proj):
        super().__init__(parent)

        self.proj = proj

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.customContextMenuRequested.connect(self.right_clicked_menu)


    def fresh_proj(self, proj):
        self.proj = proj


    def fresh_data(self):

        self.proj.fresh_model_config()
        model_config = self.proj.model_config

        model = ModelListStandardModel(self.proj.proj_name)

        # 根据modelConfig文件内容生成树
        self.generate_model(model, model_config)

        self.setModel(model)

        # 模型改变即回写
        # self.model().dataChanged.connect(self.rewrite_model)

    def generate_model(self, parent, data: list):
        """
        根据data生成树接节点
        :param parent:
        :param data:
        :return:
        """
        for item in data:
            root = ModelListStandardItem(parent, item.get('name'), item.get('is_dir'), item.get('path'))
            if item.get('is_dir'):
                self.generate_model(root, item.get('items'))

    def rewrite_model(self):
        """
        树窗体模型回写
        :return:
        """
        self.model().rewrite_config()


    def right_clicked_menu(self, pos):
        """
        右击菜单栏
        """
        index = self.indexAt(pos)
        item = self.model().itemFromIndex(index)

        # 事件定义
        menu = QMenu()
        add_child_model_action = QAction("新增模型", menu)
        add_child_dir_action = QAction("新增文件夹", menu)
        add_premodel_action = QAction('在前面插入模型', menu)
        add_postmodel_action = QAction('在后面插入模型', menu)
        delete_model_action = QAction("删除模型", menu)
        delete_dir_action = QAction("删除文件夹", menu)

        # 绑定事件
        add_child_model_action.triggered.connect(self.add_child_model_event)
        add_child_dir_action.triggered.connect(self.add_child_dir_event)
        add_premodel_action.triggered.connect(self.add_premodel_event)
        add_postmodel_action.triggered.connect(self.add_postmodel_event)
        delete_model_action.triggered.connect(self.delete_model_event)
        delete_dir_action.triggered.connect(self.delete_dir_event)

        if index.isValid():
            if item.is_dir:
                # 右击文件夹
                menu.addAction(add_child_model_action)
                menu.addAction(add_child_dir_action)
                menu.addAction(delete_dir_action)
            else:
                # 右击模型
                menu.addAction(add_premodel_action)
                menu.addAction(add_postmodel_action)
                menu.addAction(delete_model_action)

        else:
            # 点击空白处显示新增模型或者新增文件夹
            menu.addAction(add_child_model_action)
            menu.addAction(add_child_dir_action)

        menu.exec_(self.viewport().mapToGlobal(pos))

    """拖拽控制"""


    def dropEvent(self, event):
        """
        拖拽后放置控制
        不允许将节点放置到模型节点下
        """

        drop_position = self.dropIndicatorPosition()
        target_index = self.indexAt(event.pos())
        target_item = self.model().itemFromIndex(target_index)

        # 放置节点的限制
        if drop_position == QAbstractItemView.OnItem and target_item.is_dir is False:
            # 不允许放在model节点内
            Log.logger.warning(f'模型不允许放置在非文件夹的节点内')
            event.ignore()
            return

        # super().dropEvent(event)
        event.accept()

        model = self.model()
        children = model.children()
        for row in range(model.rowCount()):
            cur = model.item(row)
            node_name = cur.text()
            node_type = type(cur)
            node_parent_type = type(cur.parent())

            Log.logger.warning(f'name:{node_name}, type:{node_type}, node_parent_type:{node_parent_type}')

        # self.rewrite_model()


    """事件"""

    def add_child_model_event(self):
        pass

    def add_child_dir_event(self):
        pass

    def add_premodel_event(self):
        pass

    def add_postmodel_event(self):
        pass

    def delete_model_event(self):
        pass

    def delete_dir_event(self):
        pass
