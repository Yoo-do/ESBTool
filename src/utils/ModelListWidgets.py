from PyQt5.QtWidgets import QTreeView, QAction, QMenu, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QDataStream, QIODevice, QModelIndex
import hashlib

from src.utils import FileIO, Log


class ModelListStandardItem(QStandardItem):
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
        new_item = ModelListStandardItem(self.text(), self.is_dir, self.path)
        self.clone_all(new_item, self)

        return new_item


    def clone_all(self, clone_item, self_item):
        """
        递归复制对象子对象
        """
        for row in range(self_item.rowCount()):
            curr_item = self_item.child(row)
            new_item = ModelListStandardItem(curr_item.text(), curr_item.is_dir, clone_item.path)
            clone_item.appendRow(new_item)
            if curr_item.rowCount() > 0:
                self.clone_all(new_item, curr_item)


class ModelListStandardModel(QStandardItemModel):
    def __init__(self, proj_name):
        super().__init__()
        self.headers = ['模型']
        self.setHorizontalHeaderLabels(self.headers)
        self.proj_name = proj_name


    def rewrite_config(self):
        """
        回写modelConfig
        """

        config = self.generate_config(self)
        FileIO.ProjIO.rewrite_model_config(self.proj_name, config)



    def generate_config(self, parent):
        """
        递归解析模型展示树
        """
        dirs = []
        files = []

        global item

        # 获取item
        for row in range(parent.rowCount()):
            if isinstance(parent, ModelListStandardModel):
                item = parent.item(row)
            elif isinstance(parent, ModelListStandardItem):
                item = parent.child(row)


            # 获取item的属性值
            model_name = item.text()
            is_dir = item.is_dir
            path = item.path
            full_path = item.get_full_name()


            if is_dir:
                # 文件夹的话需要递归
                dirs.append({"name": model_name, "is_dir": is_dir, "items": self.generate_config(item)})
            else:
                # 对于修改了位置的文件进行处理 实际文件路径为逻辑路径经过md5处理
                target_path = hashlib.md5(full_path.__str__().encode()).hexdigest()
                
                if path != target_path:
                    FileIO.ProjIO.rename_model(self.proj_name, path, target_path)

                files.append({"name": model_name, "is_dir": is_dir, "path": target_path})

        return dirs.__add__(files)


class ModelListTreeView(QTreeView):
    def __init__(self, parent, proj):
        super().__init__(parent)

        self.proj = proj
        self.standard_model = None

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QTreeView.ExtendedSelection)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.customContextMenuRequested.connect(self.right_clicked_menu)

    def fresh_proj(self, proj):
        self.proj = proj

    def fresh_data(self, expanded_indexes: list[QModelIndex] = None):
        """
        刷新窗体数据，如果传入了expand_index,则展开该文件夹
        """

        if self.standard_model is not None:
            # 清除已有数据
            self.standard_model.clear()

        # 刷新model配置信息
        self.proj.fresh_model_config()

        # 创建model
        model = ModelListStandardModel(self.proj.proj_name)
        # 根据modelConfig文件内容生成树,填充model内容
        self.generate_model(model, self.proj.model_config)
        # 设置model
        self.setModel(model)

        if expanded_indexes is not None:
            """如果传入已展开的index则依次展开 待测试"""
            for expand_index in expanded_indexes:
                if expand_index.isValid():
                    self.expand(self.model().index(expand_index.row(), expand_index.column()))
                else:
                    Log.logger.info(f'展开QModelIndex无效, row:{expand_index.row()}, column:{expand_index.column()}')

    def generate_model(self, parent, data: list):
        """
        根据data生成树接节点
        :param parent:
        :param data:
        :return:
        """
        for item in data:
            root = ModelListStandardItem(item.get('name'), item.get('is_dir'), item.get('path'))
            parent.appendRow(root)
            if item.get('is_dir'):
                self.generate_model(root, item.get('items'))

    def rewrite_config(self):
        """
        modelConfig文件回写
        :return:
        """

        self.model().rewrite_config()
        self.fresh_data(self.get_expanded_indexes())

    def get_expanded_indexes(self):
        expanded_indexes = []
        model = self.model()
        def traverse(index):
            if index.isValid():
                # 检查节点是否展开
                if self.isExpanded(index):
                    expanded_indexes.append(index)

                # 遍历子节点
                for row in range(model.rowCount(index)):
                    child_index = model.index(row, 0, index)
                    traverse(child_index)

        traverse(model.index(0, 0))

        return expanded_indexes


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
        duplicate_model_action = QAction("复制模型", menu)
        rename_model_action = QAction("重命名模型", menu)
        delete_dir_action = QAction("删除文件夹", menu)
        rename_dir_action = QAction("重命名文件夹", menu)

        # 绑定事件
        add_child_model_action.triggered.connect(self.add_child_model_event)
        add_child_dir_action.triggered.connect(self.add_child_dir_event)
        add_premodel_action.triggered.connect(self.add_premodel_event)
        add_postmodel_action.triggered.connect(self.add_postmodel_event)
        delete_model_action.triggered.connect(self.delete_model_event)
        duplicate_model_action.triggered.connect(self.duplicate_model_event)
        rename_model_action.triggered.connect(self.rename_model_event)
        delete_dir_action.triggered.connect(self.delete_dir_event)
        rename_dir_action.triggered.connect(self.rename_dir_event)

        if index.isValid():
            if item.is_dir:
                # 右击文件夹 新增模型、新增文件夹、重命名文件夹、删除文件夹
                menu.addAction(add_child_model_action)
                menu.addAction(add_child_dir_action)
                menu.addAction(rename_dir_action)
                menu.addAction(delete_dir_action)
            else:
                # 右击模型 在前面插入模型、在后面插入模型、复制模型、重命名模型、删除模型
                menu.addAction(add_premodel_action)
                menu.addAction(add_postmodel_action)
                menu.addAction(duplicate_model_action)
                menu.addAction(rename_model_action)
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
            parent = target_item.parent()
            if parent is None:
                parent = self.model()

            parent.insertRow(target_index.row(), source_item.clone())

        elif drop_position == QAbstractItemView.BelowItem:
            """拖拽到下方时"""
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

        self.rewrite_config()

    def is_name_exists(self, name_path: list, name: str) -> bool:
        """
        name_path为目标层级，例如根层级为[] 判断该层级是否有重名
        """

        curr_path = self.proj.model_config
        print(name)

        if len(name_path) > 0:
            for curr_name in name_path:
                print(curr_path)
                curr_path = [path for path in curr_path if path.get('name') == curr_name][0].get('items')

        names = [path.get('name') for path in curr_path]
        print(name)
        print(names)

        if name in names:
            return False
        else:
            return True

    def generate_new_name(self, name_path: list, name: str = None) -> str:
        """
        生成新名称，若传入name，则根据name取新名称
        """
        print(f'{name_path}, {name}')
        num = 1
        if len(name) == 0:
            new_name = 'new ' + num.__str__()
            while not self.is_name_exists(name_path, new_name):
                num += 1
                new_name = 'new ' + num.__str__()
            return new_name
        else:
            num += 1
            new_name = name + f'({num.__str__()})'
            while not self.is_name_exists(name_path, new_name):
                num += 1
                new_name = name + f'({num.__str__()})'
            return new_name

    """事件"""

    def add_child_model_event(self):
        pass

    def add_child_dir_event(self):


        if len(self.selectedIndexes()) == 0:
            """即选中空白处"""
            name = self.generate_new_name([], '文件夹 ')
            item = ModelListStandardItem(name, True)
            self.model().appendRow(item)
        else:
            index = self.currentIndex().parent()
            parent = self.model().itemFromIndex(index)
            name = self.generate_new_name(parent.get_full_name, '文件夹 ')
            item = ModelListStandardItem(name, True)
            index.appendRow(item)

        self.rewrite_config()

    def add_premodel_event(self):
        pass

    def add_postmodel_event(self):
        pass

    def delete_model_event(self):
        pass

    def duplicate_model_event(self):
        pass

    def rename_model_event(self):
        pass

    def delete_dir_event(self):
        pass

    def rename_dir_event(self):
        pass
