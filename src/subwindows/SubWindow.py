from PyQt5.QtWidgets import QWidget, QMainWindow, QStackedWidget, QBoxLayout, QLabel, QListWidget, QPushButton, QTreeWidget, QTreeWidgetItem
from PyQt5.Qt import Qt, QThread, pyqtSignal
from enum import Enum
from src.utils import Data, DiyWidgets


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
    def __init__(self, main_window: QMainWindow):
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
    def __init__(self, main_window: QMainWindow):
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

        self.model_list = QListWidget(self)
        self.model_list.itemClicked.connect(self.model_selected_event)
        model_list_layout.addWidget(self.model_list)

        model_list_button_layout = QBoxLayout(QBoxLayout.LeftToRight)
        model_list_layout.addLayout(model_list_button_layout)

        self.model_add_button = QPushButton('新增', self)
        model_list_button_layout.addWidget(self.model_add_button)

        self.model_delete_button = QPushButton('删除', self)
        model_list_button_layout.addWidget(self.model_delete_button)


        # 模型细节

        # 模型细节布局
        model_detail_layout = QBoxLayout(QBoxLayout.TopToBottom, self)
        main_layout.addLayout(model_detail_layout)
        main_layout.setStretchFactor(model_detail_layout, 4)
        # 模型细节按钮组布局
        model_detail_button_layout = QBoxLayout(QBoxLayout.LeftToRight, self)
        model_detail_layout.addLayout(model_detail_button_layout)

        self.model_detail_add_node = QPushButton('新增节点', self)
        model_detail_button_layout.addWidget(self.model_detail_add_node)

        self.model_detail_delete_node = QPushButton('删除节点', self)
        model_detail_button_layout.addWidget(self.model_detail_delete_node)

        # 模型节点展示
        self.model_detial_tree = DiyWidgets.ModelNodeTreeWidget(self)

        model_detail_layout.addWidget(self.model_detial_tree)




    def fresh_data(self):
        self.model_list.clear()

        if self.main_window.curr_proj is not None:
            models = [model.model_name for model in self.main_window.curr_proj.models]
            self.model_list.addItems(models)


    def fresh_model_detail(self, data: dict):
        """
        刷新节点数据
        """
        self.model_detial_tree.clear()
        if data is None:
            return

        self.root = self.generate_tree(self.model_detial_tree, data, '根节点')



    def generate_tree(self, parent, data, name='Items') -> QTreeWidgetItem:
        try:
            if data['type'] == 'object':
                root = QTreeWidgetItem(parent)
                root.setText(0, name)
                root.setText(1, data['type'])
                for key, value in data['properties'].items():
                    self.generate_tree(root, value, key)
            elif data['type'] == 'array':
                root = QTreeWidgetItem(parent)
                root.setText(0, name)
                root.setText(1, data['type'])
                self.generate_tree(root, data['items'])
            else:
                root = QTreeWidgetItem(parent)
                root.setText(0, name)
                root.setText(1, data['type'])
                root.setText(2, data['tittle'])
                root.setText(3, data['description'])
        except Exception as e:
            raise Exception('节点:' + name + ' ' + e.__str__())


    """事件"""

    def model_selected_event(self):
        model_name =self.model_list.currentItem().text()
        data = [model.model for model in self.main_window.curr_proj.models if model.model_name == model_name][0]

        self.fresh_model_detail(data)




class SubWindow:
    """
    子窗口管理类
    """

    def __init__(self, main_window: QMainWindow):
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
