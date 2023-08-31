import json

from PyQt5.QtWidgets import QDialog, QListWidget, QBoxLayout, QDialogButtonBox, \
    QTreeWidget, QTreeWidgetItem, QStyledItemDelegate, QComboBox, QTreeView, QMessageBox, QInputDialog, QTextEdit, \
    QPushButton, QAction, QMenu, QAbstractItemView, QMainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QModelIndex

from src.utils import Data, Log


class ListDialog(QDialog):
    def __init__(self, parent, tittle, items):
        """
        弹窗列表
        """

        super().__init__(parent)

        self.show()
        self.setWindowTitle(tittle)

        layout = QBoxLayout(QBoxLayout.TopToBottom)

        self.list_widget = QListWidget()
        self.list_widget.addItems(items)
        layout.addWidget(self.list_widget)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)


class ModelLisTWidget(QListWidget):
    """
    模型列表窗体类
    """

    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.right_mouse_clicked)

        # 双击也进入重命名
        self.itemDoubleClicked.connect(self.model_item_rename_event)

    def parent_fresh_data(self):
        """
        刷新父类数据
        :return:
        """
        self.parent().fresh_data()

    def parent_fresh_proj(self):
        self.curr_proj: Data.Proj = self.parent().main_window.curr_proj

    def right_mouse_clicked(self, pos):
        """
        右击菜单栏
        :param pos:
        :return:
        """

        item = self.itemAt(pos)
        menu = QMenu(self)
        menu.show()
        if item is not None:
            rename_action = QAction("重命名")
            rename_action.triggered.connect(self.model_item_rename_event)
            delete_action = QAction("删除模型")
            delete_action.triggered.connect(self.model_item_delete_event)
            menu.addAction(rename_action)
            menu.addAction(delete_action)

        else:
            add_action = QAction("新增模型")
            add_action.triggered.connect(self.model_item_add_event)
            menu.addAction(add_action)

        action = menu.exec_(self.mapToGlobal(pos))

    """事件"""

    def model_item_rename_event(self):
        """
        重命名模型事件
        :return:
        """
        self.parent_fresh_proj()

        curr_item = self.currentItem()
        curr_model_name = curr_item.text()
        curr_model: Data.Model = [model for model in self.curr_proj.models if model.model_name == curr_model_name][0]

        target_model_name, ok = QInputDialog.getText(self, '重命名', '请输入新的名称:', text=curr_model_name)
        if ok:
            if target_model_name not in [model.model_name for model in self.curr_proj.models if
                                         model.model_name != curr_model_name]:
                curr_model.rename(target_model_name)
            else:
                QMessageBox.critical(self, '错误消息', '该名称已重复')

        self.parent_fresh_data()

    def model_item_delete_event(self):
        """
        删除模型事件
        :return:
        """
        self.parent_fresh_proj()

        curr_item = self.currentItem()
        curr_model_name = curr_item.text()

        self.curr_proj.delete_model(curr_model_name)

        self.parent_fresh_data()

    def model_item_add_event(self):
        """
        新增模型
        :return:
        """
        self.parent_fresh_proj()

        model_names = []
        count = self.count()
        for index in range(count):
            model_names.append(self.item(index).text())

        # 默认名称为new xx
        target_name = 'new ' + count.__str__()
        while target_name in model_names:
            count += 1
            target_name = 'new ' + count.__str__()

        self.curr_proj.add_model(target_name)

        self.parent_fresh_data()


class DataTypeCombox(QStyledItemDelegate):
    """
    数据类型下拉框
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.data_types = Data.ModelDataTypes

    def createEditor(self, parent, option, index):
        """
        创建
        """

        editor = QComboBox(parent)
        editor.addItems(self.data_types)

        # 当前数据类型值
        self.curr_data_type = index.model().data(index, role=Qt.DisplayRole)
        target_index = self.data_types.index(self.curr_data_type)
        editor.setCurrentIndex(target_index)

        return editor

    def setEditorData(self, editor, index):
        """
        编辑
        """
        value = index.model().data(index, role=Qt.DisplayRole)
        target_index = self.data_types.index(value)
        editor.setCurrentIndex(target_index)

    def setModelData(self, editor, model, index):
        """
        回写
        """
        tree_view: ModelTreeView = editor.parent().parent()
        item = tree_view.model().itemFromIndex(index)
        parent: ModelStandardItem = item.parent()

        # 原数据类型
        source_data_type = parent.child(index.row(), 1).text()

        # 回写模型
        value = editor.currentText()
        model.setData(index, value, role=Qt.EditRole)

        if source_data_type != value:
            tree_view.transfer_data_type(index, source_data_type, target_data_type=value)


class ModelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("导入模型")

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("请输入JSON文本")

        # 创建按钮
        self.format_button = QPushButton("格式化JSON")
        self.format_button.clicked.connect(self.format_json_event)
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)

        # 窗体布局
        layout = QBoxLayout(QBoxLayout.TopToBottom, self)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.format_button)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

    def format_json_event(self):
        """
        格式化json事件
        :return:
        """
        json_text = self.text_edit.toPlainText()
        try:
            parsed = json.loads(json_text)
            formatted_json = json.dumps(parsed, indent=4, ensure_ascii=False)
            self.text_edit.setPlainText(formatted_json)
        except json.JSONDecodeError:
            QMessageBox.warning(self, "错误", "无效的JSON文本")

    def accept(self):
        json_text = self.text_edit.toPlainText()
        try:
            self.data = json.loads(json_text)
            super().accept()
        except json.JSONDecodeError:
            QMessageBox.critical(self, "错误", "无效的JSON文本")
        except Exception as e:
            QMessageBox.critical(self, "错误", e.__str__())

    def reject(self):
        super().reject()


class ModelTreeView(QTreeView):
    """
    模型展示窗体
    实现了拖拽功能
    """

    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.customContextMenuRequested.connect(self.right_clicked_menu)

    def setModel(self, model):
        super().setModel(model)
        # 选中结点信息展示
        self.selectionModel().currentChanged.connect(self.show_node_info)

    def show_info(self, info: str):
        """
        展示信息
        """
        if self.parent() is not None and hasattr(self.parent(), 'main_window') and isinstance(self.parent().main_window,
                                                                                              QMainWindow):
            self.parent().main_window.show_status_info(info)

    def right_clicked_menu(self, pos):
        """
        右击菜单栏
        """
        index = self.indexAt(pos)

        # 点击空白处无不做反应
        if self.model().itemFromIndex(index) is None:
            return

        parent: ModelStandardItem = self.model().itemFromIndex(index).parent()

        if index.isValid():
            menu = QMenu()
            add_child_action = QAction("新增子节点", menu)
            add_prenode_action = QAction('在前面插入节点', menu)
            add_postnode_action = QAction('在后面插入节点', menu)
            delete_action = QAction("删除节点", menu)

            # 绑定事件
            add_child_action.triggered.connect(self.add_child_node_event)
            delete_action.triggered.connect(self.delete_node_event)
            add_prenode_action.triggered.connect(self.add_pre_node_event)
            add_postnode_action.triggered.connect(self.add_post_node_event)

            # 按节点分配菜单按钮
            if parent is None:
                # 根节点不支持任何操作
                pass
            elif parent.child(index.row(), 1).data(role=Qt.DisplayRole) == 'object':

                # object 类型节点
                # 区分一下数组中的object

                parent_data_type = parent.get_data_type()
                if parent_data_type == 'array':
                    menu.addAction(add_child_action)
                else:
                    menu.addAction(add_child_action)
                    menu.addAction(add_prenode_action)
                    menu.addAction(add_postnode_action)
                    menu.addAction(delete_action)

            elif parent.child(index.row(), 1).data(role=Qt.DisplayRole) == 'array':
                # array 类型节点
                menu.addAction(add_prenode_action)
                menu.addAction(add_postnode_action)
                menu.addAction(delete_action)

            elif parent.child(index.row(), 1).data(role=Qt.DisplayRole) not in ['object', 'array']:
                # 普通节点
                menu.addAction(add_prenode_action)
                menu.addAction(add_postnode_action)
                menu.addAction(delete_action)

            menu.exec_(self.viewport().mapToGlobal(pos))

    def transfer_data_type(self, index: QModelIndex, source_data_type, target_data_type):
        """
        类型转换
        """
        parent: ModelStandardItem = self.model().itemFromIndex(index).parent()
        row = index.row()
        item_name = parent.child(row, 0).text()

        if source_data_type not in ['object', 'array']:
            if target_data_type not in ['object', 'array']:
                # 普通类型转换 无任何额外操作
                pass
            elif target_data_type in ['object', 'array']:
                # 普通类型转换成 object, array 类型

                # 关闭必填类型，并设置为不可编辑
                parent.setChild(row, 2, QStandardItem())
                parent.child(row, 2).setEditable(False)

                if target_data_type == 'array':
                    # 如果是array类型则需要额外增加一个item子节点

                    # curr_item = parent.child(row, 0)
                    # ModelStandardItem(self, curr_item, 'items', 'object', True)
                    curr_index = index
                    curr_item = self.model().itemFromIndex(index).parent().child(curr_index.row(), 0)
                    Log.logger.info(curr_item.text())
                    Log.logger.info(type(curr_item))
                    # ModelStandardItem(self, curr_item, 'items', 'object', True)

        Log.logger.info(f'{item_name}的类型由 [{source_data_type}] 转换成 [{target_data_type}]')

    def startDrag(self, supported_action):
        """
        重写开始拖拽方法
        禁用部分特殊结点的拖拽功能
        """
        index = self.currentIndex()
        parent = self.model().itemFromIndex(index).parent()

        if parent is None:
            # 根节点禁止拖拽
            return

        column_name = parent.child(index.row(), 0).data(role=Qt.DisplayRole)
        data_type = parent.child(index.row(), 1).data(role=Qt.DisplayRole)

        if column_name == "items" and data_type == 'object':
            # 数组内items结点不允许拖动
            return
        else:
            super().startDrag(supported_action)

    def dropEvent(self, event):

        drop_position = self.dropIndicatorPosition()

        target_index = self.indexAt(event.pos())
        target_parent = self.model().itemFromIndex(target_index).parent()

        if target_parent is None:
            if drop_position in [QAbstractItemView.AboveItem, QAbstractItemView.BelowItem]:
                Log.logger.warning('禁止拖拽到根节点外')
                event.ignore()
                return
            elif drop_position == QAbstractItemView.OnItem:
                super().dropEvent(event)
                return

        target_data_type = target_parent.child(target_index.row(), 1).data(role=Qt.DisplayRole)

        # 放置节点的限制
        if drop_position == QAbstractItemView.OnItem and target_data_type not in ['object']:
            # 不允许放在非object节点内
            Log.logger.warning(f'不允许放置在 {target_data_type} 节点内')
            event.ignore()
            return
        elif drop_position in [QAbstractItemView.AboveItem, QAbstractItemView.BelowItem]:
            # 拖拽到上下侧时 禁止直接拖到数组的节点里，必须拖拽到items里面

            target_parent_index = target_parent.index()
            target_parent_parent: ModelStandardItem = target_parent.parent()
            if isinstance(target_parent_parent, QStandardItem):
                # 不满足这个条件的不进行判断
                target_parent_parent_data_type = target_parent_parent.child(target_parent_index.row(), 1).data(
                    role=Qt.DisplayRole)
                if target_parent_parent_data_type == 'array':
                    Log.logger.warning(f'不允许直接放置节点到 array 节点里，必须放置到items里')

                    event.ignore()
                    return

        super().dropEvent(event)

    def show_node_info(self, current, previous):
        """
        信息展示
        """
        result = '父级:[{}] '.format(str(current.parent().data()))
        result += '当前选中:[(行{},列{})] '.format(current.row(), current.column())

        name = ''
        info = ''
        if current.column() == 0:
            name = str(current.data())
            info = str(current.sibling(current.row(), 1).data())
        else:
            name = str(current.sibling(current.row(), 0).data())
            info = str(current.data())

        result += '名称:[{}]  类型:[{}]'.format(name, info)

        self.show_info(result)

    def delete_node_event(self):
        """
        删除结点
        """
        index = self.currentIndex()
        if index.isValid():
            self.model().removeRow(index.row(), index.parent())

    def add_child_node_event(self):
        """
        新增子结点
        """
        index = self.currentIndex()
        curr_item = self.model().itemFromIndex(index).parent().child(index.row(), 0)
        if index.isValid():
            # 执行新增节点的操作
            ModelStandardItem(self, curr_item, '新结点', 'string', True)

    def add_pre_node_event(self):
        """
        在目标节点前面增加节点
        :return:
        """
        index = self.currentIndex()
        if index.isValid():
            parent = self.model().itemFromIndex(index).parent()
            row = index.row()
            ModelStandardItem(self, parent, '新结点', 'string', True, row=row)

            # 日志输出
            Log.logger.debug(f'新增节点')

    def add_post_node_event(self):
        """
        在目标节点后面增加节点
        :return:
        """
        index = self.currentIndex()
        if index.isValid():
            parent = self.model().itemFromIndex(index).parent()
            row = index.row() + 1
            ModelStandardItem(self, parent, '新结点', 'string', True, row=row)

            # 日志输出
            Log.logger.debug(f'新增节点')


class ModelStandardItem(QStandardItem):
    """
    模型节点类
    """

    def __init__(self, tree_view: QTreeView, parent: QStandardItemModel | QStandardItem, item_name: str, data_type: str,
                 is_required: bool, cn_name: str = None, description: str = None, row: int = None):
        """
        非object、array类型,则带kwargs: is_required: bool, cn_name: str, description: str
        """

        super().__init__(item_name)
        if isinstance(parent, QStandardItemModel):
            # 根节点限制编辑
            self.setEditable(False)

        self.tree_view = tree_view

        # row 赋值
        row = parent.rowCount() if row is None else row

        if data_type in ['object', 'array']:
            self.dir_node_init(parent, data_type, cn_name, description, row)
        else:
            self.leaf_node_init(parent, data_type, is_required, cn_name, description, row)

    def get_data_type(self):
        """
        获取当前行的类型
        """
        if self.parent() is not None:
            index = self.index()
            return self.parent().child(index.row(), 1).data(role=Qt.DisplayRole)

    def get_column_name(self):
        """
        获取当前行的名称
        """
        if self.parent() is not None:
            index = self.index()
            return self.parent().child(index.row(), 0).data(role=Qt.DisplayRole)

    def dir_node_init(self, parent, data_type: str, cn_name: str, description: str, row: int):
        """
        目录结点初始化 该节点都是必须，所以不设置必须选项
        """

        data_type_item = QStandardItem(data_type)
        self.tree_view.setItemDelegateForColumn(1, DataTypeCombox())

        cn_name_item = QStandardItem(cn_name)
        description_item = QStandardItem(description)

        if isinstance(parent, QStandardItemModel):
            # 根节点限制编辑
            data_type_item.setEditable(False)
            cn_name_item.setEditable(False)
            description_item.setEditable(False)

        # 插入到指定行
        parent.insertRow(row, self)

        # object、array类型不允许修改类型
        if isinstance(parent, self.__class__):
            parent.setChild(row, 1, data_type_item)
            # 不允许修改类型
            parent.child(row, 1).setEditable(False)
            # 限制编辑
            parent.setChild(row, 2, QStandardItem())
            parent.child(row, 2).setEditable(False)

            parent.setChild(row, 3, cn_name_item)
            parent.setChild(row, 4, description_item)
        elif isinstance(parent, ModelStandardItem | QStandardItemModel):
            parent.setItem(row, 1, data_type_item)
            # 不允许修改类型
            parent.item(row, 1).setEditable(False)
            # 限制编辑
            parent.setItem(row, 2, QStandardItem())
            parent.item(row, 2).setEditable(False)

            parent.setItem(row, 3, cn_name_item)
            parent.setItem(row, 4, description_item)

    def leaf_node_init(self, parent, data_type: str, is_required: bool, cn_name: str, description: str, row: int):
        """
        叶子结点初始化
        """
        data_type_item = QStandardItem(data_type)
        self.tree_view.setItemDelegateForColumn(1, DataTypeCombox())

        is_required_item = QStandardItem()
        is_required_item.setEditable(False)
        is_required_item.setCheckable(True)
        is_required_item.setCheckState(Qt.Checked if is_required else Qt.Unchecked)

        cn_name_item = QStandardItem(cn_name)
        description_item = QStandardItem(description)

        # 插入到指定行
        parent.insertRow(row, self)

        parent.setChild(row, 1, data_type_item)
        parent.setChild(row, 2, is_required_item)
        parent.setChild(row, 3, cn_name_item)
        parent.setChild(row, 4, description_item)


class ModelStandardModel(QStandardItemModel):
    def __init__(self):
        super().__init__()
        self.headers = ['节点', '类型', '必选', '中文名', '描述']
        self.setHorizontalHeaderLabels(self.headers)

    def __jsonschema__(self):
        """
        转成对应的jsonschema
        :return:
        """
        if self.rowCount() == 1:
            root = self.item(0)
            data_type = self.item(0, 1).text()

            properties, required = self.generate_json(root, True)
            result = {"type": data_type, "properties": properties, "required": required}
            return result

    def generate_json(self, item: QStandardItem, is_object=False):
        """
        递归解析ModelStandardModel
        在上级type为object时, is_object为True
        在type为object时返回:properties, required
        其他时返回: result
        """

        try:
            result = {}
            required = []
            if item.rowCount() > 0:
                for index in range(item.rowCount()):
                    child = item.child(index)
                    col_name = None if item.child(index, 0) is None else item.child(index, 0).text()
                    data_type = None if item.child(index, 1) is None else item.child(index, 1).text()

                    require_state = None if item.child(index, 2) is None else item.child(index, 2).checkState()
                    if require_state == Qt.Checked:
                        require = True
                        required.append(col_name)
                    elif require_state == Qt.Unchecked:
                        require = False
                    else:
                        require = None

                    tittle = None if item.child(index, 3) is None else item.child(index, 3).text()
                    description = None if item.child(index, 4) is None else item.child(index, 4).text()
                    if item.child(index).rowCount() == 0:
                        result.update({col_name: {"type": data_type, "tittle": tittle, "description": description,
                                                  "require": require}})
                    else:
                        if data_type == 'array':
                            # array类型的默认加入required
                            required.append(col_name)
                            # 数组类型的往下再取一个节点
                            res = {"type": data_type}
                            res.update({"items": next(iter(self.generate_json(child).values()))})
                            result.update({col_name: res})
                        elif data_type == 'object':
                            child_properties, child_required = self.generate_json(child, True)
                            result.update({col_name: {"type": data_type, "properties": child_properties,
                                                      "required": child_required}})

            if is_object:
                return result, required
            return result


        except Exception as e:
            raise Exception("节点: ", item.child(0, 0).text(), "报错：", e.__str__())
