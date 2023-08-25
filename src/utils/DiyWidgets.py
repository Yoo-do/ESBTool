import json

from PyQt5.QtWidgets import QDialog, QListWidget, QBoxLayout, QDialogButtonBox, \
    QTreeWidget, QTreeWidgetItem, QStyledItemDelegate, QComboBox, QTreeView, QMessageBox, QInputDialog, QTextEdit, QPushButton, QAction,QMenu
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

from src.utils import Data


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
            delete_action = QAction("删除")
            delete_action.triggered.connect(self.model_item_delete_event)
            menu.addAction(rename_action)
            menu.addAction(delete_action)

        else:
            add_action = QAction("新增")
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
            if target_model_name not in [model.model_name for model in self.curr_proj.models if model.model_name != curr_model_name]:
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

    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.addItems(Data.ModelDataTypes)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, role=Qt.DisplayRole)
        editor.setCurrentText(value)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, role=Qt.EditRole)


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
    """

    def __init__(self, parent):
        super().__init__(parent=parent)


class ModelStandardItemDir(QStandardItem):
    """
    模型文件类
    """

    def __init__(self, tree_view: QTreeView, parent: QStandardItem | QStandardItemModel, dir_name, data_type):
        super().__init__(dir_name)
        self.data_type_item = QStandardItem(data_type)
        tree_view.setItemDelegateForColumn(1, DataTypeCombox())

        parent.appendRow(self)
        if isinstance(parent, self.__class__):
            parent.setChild(parent.rowCount() - 1, 1, self.data_type_item)
        elif isinstance(parent, ModelStandardModel):
            parent.setItem(parent.rowCount() - 1, 1, self.data_type_item)


class ModelStandardItemNode(QStandardItem):
    """
    模型节点类
    """

    def __init__(self, tree_view: QTreeView, parent: QStandardItem, node_name, data_type,
                 is_required: bool, cn_name, description):
        super().__init__(node_name)
        self.data_type_item = QStandardItem(data_type)

        self.is_required_item = QStandardItem()
        self.is_required_item.setCheckable(True)
        self.is_required_item.setCheckState(Qt.Checked if is_required else Qt.Unchecked)

        self.cn_name_item = QStandardItem(cn_name)
        self.description_item = QStandardItem(description)

        tree_view.setItemDelegateForColumn(1, DataTypeCombox())

        parent.appendRow(self)
        parent.setChild(parent.rowCount() - 1, 1, self.data_type_item)
        parent.setChild(parent.rowCount() - 1, 2, self.is_required_item)
        parent.setChild(parent.rowCount() - 1, 3, self.cn_name_item)
        parent.setChild(parent.rowCount() - 1, 4, self.description_item)

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
                        result.update({col_name: {"type": data_type, "tittle": tittle, "description": description, "require": require}})
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
                            result.update({col_name: {"type": data_type, "properties": child_properties, "required": child_required}})

            if is_object:
                return result, required
            return result


        except Exception as e:
            raise Exception("节点: ", item.child(0, 0).text(), "报错：", e.__str__())

