from PyQt5.QtWidgets import QTreeView, QAction, QMenu, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from src.utils import FileIO

class ModelListStandardItem(QStandardItem):
    def __init__(self, parent: QStandardItemModel | QStandardItem, name: str, is_dir: bool, path: str = None):
        super().__init__(name)
        self.is_dir = is_dir
        self.path = path
        parent.appendRow(self)

    def get_full_name(self):
        """
        获取模型的绝对逻辑路径
        :return:
        """
        path = []
        parent = self.parent()
        while parent is not None:
            path.insert(parent.name)
            parent = parent.parent()

        path.append(self.text())
        return path



class ModelListStandardModel(QStandardItemModel):
    def __init__(self):
        super().__init__()
        self.headers = ['名称']
        self.setHorizontalHeaderLabels(self.headers)


class ModelListTreeView(QTreeView):
    def __init__(self, parent):
        super().__init__(parent)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.customContextMenuRequested.connect(self.right_clicked_menu)

    def fresh_data(self, proj):
        proj.fresh_model_config()
        model_config = proj.model_config

        model = ModelListStandardModel()


        # 根据modelConfig文件内容生成树
        self.generate_model(model, model_config)

        self.setModel(model)


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


