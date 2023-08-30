from PyQt5.QtWidgets import QWidget, QMainWindow, QStackedWidget, QBoxLayout, QLabel, QListWidget, QPushButton, \
    QTreeWidget, QTreeWidgetItem, QDialog
from PyQt5.Qt import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from enum import Enum
from src.utils import Data, DiyWidgets, Log

from src.Interface import Interface


class SubWindowType(Enum):
    """
    全部子窗口类型
    """
    # 主页
    INDEX_WINDOW = 0,
    # 模型页面
    MODEL_WINDOW = 1,
    # 校验页面
    VALIDATE_WINDOW = 2,


class IndexWindow(QWidget):
    def __init__(self, main_window: Interface):
        super().__init__(main_window)
        self.main_window = main_window

        self.ui_init()
        self.fresh_data()

    def ui_init(self):
        self.show()
        layout = QBoxLayout(QBoxLayout.TopToBottom | QBoxLayout.LeftToRight, self)

        self.label = QLabel(self)
        self.label.show()
        layout.addWidget(self.label)

    def fresh_data(self):
        if self.main_window.curr_proj_name is None:
            self.label.setText('未选择项目')
        else:
            self.label.setText(self.main_window.curr_proj_name)


class ModelWindow(QWidget):
    def __init__(self, main_window: Interface):
        super().__init__(main_window)
        self.main_window = main_window

        self.ui_init()
        self.fresh_data()

    def ui_init(self):

        # 主布局，左右窗体
        main_layout = QBoxLayout(QBoxLayout.LeftToRight, self)

        # 模型列表
        model_list_layout = QBoxLayout(QBoxLayout.TopToBottom)
        main_layout.addLayout(model_list_layout)
        main_layout.setStretchFactor(model_list_layout, 1)

        self.model_list = DiyWidgets.ModelLisTWidget(self)
        self.model_list.itemClicked.connect(self.model_selected_event)
        model_list_layout.addWidget(self.model_list)

        model_list_button_layout = QBoxLayout(QBoxLayout.LeftToRight)
        model_list_layout.addLayout(model_list_button_layout)

        self.model_add_button = QPushButton('新增模型', self)
        self.model_add_button.clicked.connect(self.model_list.model_item_add_event)
        model_list_button_layout.addWidget(self.model_add_button)

        # 模型细节

        # 模型细节布局
        model_detail_layout = QBoxLayout(QBoxLayout.TopToBottom, self)
        main_layout.addLayout(model_detail_layout)
        main_layout.setStretchFactor(model_detail_layout, 4)
        # 模型细节按钮组布局
        model_detail_button_layout = QBoxLayout(QBoxLayout.LeftToRight, self)
        model_detail_layout.addLayout(model_detail_button_layout)

        self.model_import_button = QPushButton('导入json', self)
        self.model_import_button.setEnabled(False)
        self.model_import_button.clicked.connect(self.model_import_event)
        model_detail_button_layout.addWidget(self.model_import_button)

        self.model_save_button = QPushButton('保存', self)
        self.model_import_button.setEnabled(False)
        self.model_save_button.clicked.connect(self.model_save_event)
        model_detail_button_layout.addWidget(self.model_save_button)

        # 模型节点展示
        self.model_detial_tree = DiyWidgets.ModelTreeView(self)

        model_detail_layout.addWidget(self.model_detial_tree)

        # 结构模型
        self.tree_standard_model: DiyWidgets.ModelStandardModel = None

    def fresh_data(self):
        """
        刷新数据和全部数据窗体
        :return:
        """
        # 按钮状态调整
        self.model_import_button.setEnabled(False)
        self.model_save_button.setEnabled(False)

        self.model_list.clear()
        if self.tree_standard_model is not None:
            self.tree_standard_model.clear()

        if self.main_window.curr_proj is not None:
            models = [model.model_name for model in self.main_window.curr_proj.models]
            self.model_list.addItems(models)

        # 提示框删除
        self.main_window.clear_status_info()

    def fresh_model_detail(self, data: dict):
        """
        刷新节点数据
        """
        if data is None:
            return

        self.tree_standard_model = DiyWidgets.ModelStandardModel()
        self.model_detial_tree.setModel(self.tree_standard_model)
        self.model_detial_tree.header().resizeSection(0, 300)

        self.generate_tree_model(self.tree_standard_model, data, '根节点')

    def generate_tree_model(self, parent, data, name='items'):
        try:

            # 生成节点
            root = DiyWidgets.ModelStandardItem(self.model_detial_tree, parent, name, data.get('type'),
                                                data.get('require'),
                                                data.get('tittle'), data.get('description'))

            # 判断是否有子节点需要生成
            if data['type'] == 'object':
                for key, value in data['properties'].items():
                    self.generate_tree_model(root, value, key)
            elif data['type'] == 'array':
                # 数组类型默认增加一个items
                self.generate_tree_model(root, data['items'])
            else:
                pass

        except Exception as e:
            raise Exception('节点:' + name + ' ' + e.__str__())

    """事件"""

    def model_selected_event(self):
        """
        模型选中事件
        :return:
        """

        model_name = self.model_list.currentItem().text()
        data = [model.model for model in self.main_window.curr_proj.models if model.model_name == model_name][0]

        self.fresh_model_detail(data)
        self.model_detial_tree.expandAll()

        # 更新按钮状态
        self.model_import_button.setEnabled(True)
        self.model_save_button.setEnabled(True)

        self.main_window.show_status_info(f'已选中模型[{model_name}]')

    def model_save_event(self):
        """保存事件"""
        model_name = self.model_list.currentItem().text()
        curr_model: Data.Model = \
        [model for model in self.main_window.curr_proj.models if model.model_name == model_name][0]
        curr_model.save(self.tree_standard_model.__jsonschema__())

        # 信息展示
        self.main_window.show_status_info(f'模型[{model_name}]已保存')

    def model_import_event(self):
        """
        导入模型事件
        :return:
        """
        try:
            dialog = DiyWidgets.ModelDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                model_name = self.model_list.currentItem().text()
                curr_model: Data.Model = \
                [model for model in self.main_window.curr_proj.models if model.model_name == model_name][0]
                data = dialog.data
                curr_model.import_json(data)

                # 刷新节点
                self.model_selected_event()

        except Exception as e:
            print(e.__str__())

    def model_add_node(self):
        pass


class SubWindow:
    """
    子窗口管理类
    """

    def __init__(self, main_window: Interface):
        self.main_window = main_window
        self.stack_widget = QStackedWidget(main_window)
        main_window.setCentralWidget(self.stack_widget)

        # 主页窗体
        self.stack_widget.addWidget(IndexWindow(main_window))

        self.stack_widget.addWidget(ModelWindow(main_window))

    def switch_to_window(self, target_window_type: SubWindowType):
        self.stack_widget.setCurrentIndex(target_window_type.value[0])

    def fresh_all_data(self):
        for index in range(self.stack_widget.count()):
            widget = self.stack_widget.widget(index)
            widget.fresh_data()
