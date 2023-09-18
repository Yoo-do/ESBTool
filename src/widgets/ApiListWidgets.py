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
        """
        刷新项目
        """
        self.proj = proj

    def fresh_data(self, expanded_dirs: list[{}] = None):
        """
        刷新窗体数据，如果传入了expand_index,则展开该文件夹
        """

        if self.standard_model is not None:
            # 清除已有数据
            self.standard_model.clear()

        # 刷新api配置信息
        self.proj.fresh_api_config()

        # 创建model
        model = ApiListStandardModel(self.proj.proj_name)
        # 根据modelConfig文件内容生成树,填充model内容
        self.generate_model(model, self.proj.api_config)
        # 设置model
        self.setModel(model)

        if expanded_dirs is not None:
            self.expend_dirs(expanded_dirs, model)

    def generate_model(self, parent, data: list):
        """
        根据data生成树接节点
        :param parent:
        :param data:
        :return:
        """
        for item in data:
            root = ApiListStandardItem(item.get('name'), item.get('is_dir'), item.get('path'))
            parent.appendRow(root)
            if item.get('is_dir'):
                self.generate_model(root, item.get('items'))

    def rewrite_config(self):
        """
        modelConfig文件回写
        :return:
        """

        self.model().rewrite_config()
        expanded_dirs = []
        for row in range(self.model().rowCount()):
            expanded_dirs += self.get_expanded_dirs(self.model().index(row, 0))
        print(expanded_dirs)
        self.fresh_data(expanded_dirs)

    def get_expanded_dirs(self, parent_index: QModelIndex):
        expanded_dirs = []

        # 检查节点是否展开
        if self.isExpanded(parent_index):
            items = []
            # 遍历子节点
            item = self.model().itemFromIndex(parent_index)
            for row in range(item.rowCount()):
                items += self.get_expanded_dirs(item.child(row).index())
            expanded_dirs.append({"name": self.model().itemFromIndex(parent_index).text(), "items": items})

        return expanded_dirs

    def expend_dirs(self, expanded_dirs: list, parent: ApiListStandardModel | ApiListStandardItem):
        """
        按传进来的文件夹递归展开 expanded_dirs : [{"name":, "items"[{}]}]
        """
        if len(expanded_dirs) == 0:
            return

        dir_names = [dir.get('name') for dir in expanded_dirs]

        for row in range(parent.rowCount()):
            if isinstance(parent, ApiListStandardModel):
                item = parent.item(row)
            else:
                item = parent.child(row)
            if item.is_dir and item.text() in dir_names:
                # 展开对应文件夹
                self.expand(item.index())
                print(f'expand {item.text()}')
                self.expend_dirs([dir.get('items') for dir in expanded_dirs if dir.get('name') == item.text()][0], item)

    def right_clicked_menu(self, pos):
        """
        右击菜单栏
        """
        index = self.indexAt(pos)
        item = self.model().itemFromIndex(index)

        # 事件定义
        menu = QMenu()
        add_child_api_action = QAction("新增接口", menu)
        add_child_dir_action = QAction("新增文件夹", menu)
        add_preapi_action = QAction('在前面插入接口', menu)
        add_postapi_action = QAction('在后面插入接口', menu)
        delete_api_action = QAction("删除接口", menu)
        duplicate_api_action = QAction("复制接口", menu)
        rename_api_action = QAction("重命名接口", menu)
        delete_dir_action = QAction("删除文件夹", menu)
        rename_dir_action = QAction("重命名文件夹", menu)

        # 绑定事件
        add_child_api_action.triggered.connect(self.add_child_api_event)
        add_child_dir_action.triggered.connect(self.add_child_dir_event)
        add_preapi_action.triggered.connect(self.add_preapi_event)
        add_postapi_action.triggered.connect(self.add_postapi_event)
        delete_api_action.triggered.connect(self.delete_api_event)
        duplicate_api_action.triggered.connect(self.duplicate_api_event)
        rename_api_action.triggered.connect(self.rename_event)
        delete_dir_action.triggered.connect(self.delete_dir_event)
        rename_dir_action.triggered.connect(self.rename_event)

        if index.isValid():
            if item.is_dir:
                # 右击文件夹 新增模型、新增文件夹、重命名文件夹、删除文件夹
                menu.addAction(add_child_api_action)
                menu.addAction(add_child_dir_action)
                menu.addAction(rename_dir_action)
                menu.addAction(delete_dir_action)
            else:
                # 右击模型 在前面插入模型、在后面插入模型、复制模型、重命名模型、删除模型
                menu.addAction(add_preapi_action)
                menu.addAction(add_postapi_action)
                menu.addAction(duplicate_api_action)
                menu.addAction(rename_api_action)
                menu.addAction(delete_api_action)
        else:
            # 点击空白处显示新增模型或者新增文件夹
            menu.addAction(add_child_api_action)
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
                # 不允许放在api节点内
                QMessageBox.critical(self.parent(), '错误提示', f'不允许放置在接口结点内')
                event.ignore()
                return
            else:
                if target_item is not None:
                    new_item = source_item.clone()

                    if self.is_name_exists(target_item.get_full_name(), new_item.text()):
                        QMessageBox.critical(self.parent(), '错误提示', f'相同的名称"{new_item.text()}"')
                        event.ignore()
                        return

                    target_item.appendRow(new_item)
                else:
                    new_item = source_item.clone()
                    if self.is_name_exists([], new_item.text()):
                        QMessageBox.critical(self.parent(), '错误提示', f'相同的名称"{new_item.text()}"')
                        event.ignore()
                        return
                    self.model().appendRow()

        elif drop_position == QAbstractItemView.AboveItem:
            """拖拽到上方时"""
            parent = target_item.parent()
            if parent is None:
                parent = self.model()
                full_name_path = []
            else:
                full_name_path = parent.get_full_name()

            new_item = source_item.clone()
            # 目标路径有相同名称的话跳出提示框
            if self.is_name_exists(full_name_path, new_item.text()):
                QMessageBox.critical(self.parent(), '错误提示', f'相同的名称"{new_item.text()}"')
                event.ignore()
                return

            parent.insertRow(target_index.row(), new_item)

        elif drop_position == QAbstractItemView.BelowItem:
            """拖拽到下方时"""
            parent = target_item.parent()
            if parent is None:
                parent = self.model()
                full_name_path = []
            else:
                full_name_path = parent.get_full_name()

            new_item = source_item.clone()
            # 目标路径有相同名称的话跳出提示框
            if self.is_name_exists(full_name_path, new_item.text()):
                QMessageBox.critical(self.parent(), '错误提示', f'相同的名称"{new_item.text()}"')
                event.ignore()
                return

            parent.insertRow(target_index.row() + 1, new_item)

        elif drop_position == QAbstractItemView.OnViewport:
            """拖拽到空白处"""
            new_item = source_item.clone()
            if self.is_name_exists([], new_item.text()):
                QMessageBox.critical(self.parent(), '错误提示', f'相同的名称"{new_item.text()}"')
                event.ignore()
                return

            self.model().insertRow(self.model().rowCount(), new_item)

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

        curr_path = self.proj.api_config

        if len(name_path) > 0:
            for curr_name in name_path:
                curr_path = [path for path in curr_path if path.get('name') == curr_name][0].get('items')

        names = [path.get('name') for path in curr_path]

        if name in names:
            return True
        else:
            return False

    def generate_new_name(self, name_path: list, name: str = None) -> str:
        """
        生成新名称，若传入name，则根据name取新名称
        """
        num = 1
        if name is None:
            new_name = 'new ' + num.__str__()
            while self.is_name_exists(name_path, new_name):
                num += 1
                new_name = 'new ' + num.__str__()
            return new_name
        else:
            num += 1
            new_name = name + f'({num.__str__()})'
            while self.is_name_exists(name_path, new_name):
                num += 1
                new_name = name + f'({num.__str__()})'
            return new_name

    """事件"""

    def add_child_api_event(self):
        """
        新增模型
        """
        if len(self.selectedIndexes()) == 0:
            """即选中空白处"""
            name = self.generate_new_name([])
            item = ApiListStandardItem(name, False, '')
            self.model().appendRow(item)
        else:
            index = self.currentIndex()
            parent = self.model().itemFromIndex(index)
            name = self.generate_new_name(parent.get_full_name())
            item = ApiListStandardItem(name, False, '')
            parent.appendRow(item)

        self.proj.add_api(item.get_full_name())
        self.rewrite_config()

    def add_child_dir_event(self):
        """
        新增文件夹
        """
        if len(self.selectedIndexes()) == 0:
            """即选中空白处"""
            name = self.generate_new_name([], '文件夹 ')
            item = ApiListStandardItem(name, True)
            self.model().appendRow(item)
        else:
            index = self.currentIndex()
            parent = self.model().itemFromIndex(index)
            name = self.generate_new_name(parent.get_full_name(), '文件夹 ')
            item = ApiListStandardItem(name, True)
            parent.appendRow(item)

        self.rewrite_config()

    def add_preapi_event(self):
        """
        在前面插入一个接口
        """

        index = self.currentIndex()
        parent = self.model().itemFromIndex(index).parent()

        if parent is None:
            parent = self.model()
            full_name_path = []
        else:
            full_name_path = parent.get_full_name()
        name = self.generate_new_name(full_name_path)
        item = ApiListStandardItem(name, False, '')
        parent.insertRow(index.row(), item)

        self.proj.add_api(item.get_full_name())
        self.rewrite_config()

    def add_postapi_event(self):
        """
        在后面插入一个接口
        """
        index = self.currentIndex()
        parent = self.model().itemFromIndex(index).parent()

        if parent is None:
            parent = self.model()
            full_name_path = []
        else:
            full_name_path = parent.get_full_name()
        name = self.generate_new_name(full_name_path)
        item = ApiListStandardItem(name, False, '')
        parent.insertRow(index.row() + 1, item)

        self.proj.add_api(item.get_full_name())
        self.rewrite_config()


    def delete_api_event(self):
        """
        删除接口
        """
        index = self.currentIndex()
        item = self.model().itemFromIndex(index)
        self.proj.delete_api(item.get_full_name())

        if item.parent() is not None:
            item.parent().removeRow(index.row())
        else:
            self.model().removeRow(index.row())

        self.rewrite_config()

    def duplicate_api_event(self):
        """
        复制当前接口
        """
        index = self.currentIndex()
        item = self.model().itemFromIndex(index)
        new_name = self.generate_new_name(item.get_full_name()[:-1], item.text())
        new_path = self.proj.duplicate_api(item.get_full_name(), new_name)
        new_item = ApiListStandardItem(new_name, False, new_path)

        # 在当前模型后插入
        if item.parent() is not None:
            item.parent().insertRow(index.row() + 1, new_item)
        else:
            self.model().insertRow(index.row() + 1, new_item)

        self.rewrite_config()

    def rename_event(self):
        """
        重命名接口
        """
        index = self.currentIndex()
        item = self.model().itemFromIndex(index)
        api_name = item.text()
        api_name_path = item.get_full_name()
        api_name_path.pop()

        target_api_name, ok = QInputDialog.getText(self, '重命名', '请输入新的名称:', text=api_name)
        if ok:
            if self.is_name_exists(api_name_path, target_api_name) and api_name != target_api_name:
                QMessageBox.critical(self, '错误消息', '该名称已重复')
            else:
                item.setText(target_api_name)
                Log.logger.info(f'{"文件夹" if item.is_dir else "模型"} [{api_name}] 更名为 [{target_api_name}]')

        self.rewrite_config()

    def delete_dir_event(self):
        """
        删除文件夹，文件夹内部的文件只是在配置中删除了，没有实际物理删除
        """
        index = self.currentIndex()
        item = self.model().itemFromIndex(index)

        if item.parent() is not None:
            item.parent().removeRow(index.row())
        else:
            self.model().removeRow(index.row())

        self.rewrite_config()