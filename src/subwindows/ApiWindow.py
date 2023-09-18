from PyQt5.QtWidgets import QWidget, QBoxLayout, QLabel, QPushButton, QDialog, QTabWidget, QComboBox, QTextEdit
from PyQt5.QtCore import Qt

from src.widgets import ApiListWidgets


class ApiWindow(QWidget):
    """
    接口层窗口
    """

    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window

        self.ui_init()
        self.fresh_data()

    def ui_init(self):
        """
        ui初始化
        """
        # 主布局，左右窗体
        main_layout = QBoxLayout(QBoxLayout.LeftToRight, self)

        # 接口文件夹树
        self.api_list_tree = ApiListWidgets.ApiListTreeView(self, self.main_window.curr_proj)
        self.api_list_tree.clicked.connect(self.api_selected_event)
        main_layout.addWidget(self.api_list_tree)

        # 右侧选项卡
        self.tab_widget = QTabWidget(self)
        main_layout.addWidget(self.tab_widget)
        main_layout.setStretchFactor(self.tab_widget, 4)

        # “设置”选项卡
        self.tab_edit = QWidget()
        self.tab_widget.addTab(self.tab_edit, '设置')

        tab_edit_layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.tab_edit.setLayout(tab_edit_layout)

        # 设置选选项卡子窗体
        self.tabe_edit_request_tittle = QLabel('请求模型', self.tab_edit)
        self.tabe_edit_request_combox = QComboBox(self.tab_edit)
        self.tabe_edit_response_tittle = QLabel('响应模型', self.tab_edit)
        self.tabe_edit_response_combox = QComboBox(self.tab_edit)
        self.tabe_edit_description_tittle = QLabel('描述信息', self.tab_edit)
        self.tabe_edit_description_textedit = QTextEdit(self.tab_edit)
        self.tabe_edit_description_textedit.adjustSize()
        self.tabe_edit_valid_tittle = QLabel('是否废弃', self.tab_edit)
        self.tabe_edit_valid_combox = QComboBox(self.tab_edit)
        self.tabe_edit_valid_combox.addItems(['否', '是'])

        tab_edit_layout.addWidget(self.tabe_edit_request_tittle)
        tab_edit_layout.addWidget(self.tabe_edit_request_combox)
        tab_edit_layout.addWidget(self.tabe_edit_response_tittle)
        tab_edit_layout.addWidget(self.tabe_edit_response_combox)
        tab_edit_layout.addWidget(self.tabe_edit_description_tittle)
        tab_edit_layout.addWidget(self.tabe_edit_description_textedit)
        tab_edit_layout.addWidget(self.tabe_edit_valid_tittle)
        tab_edit_layout.addWidget(self.tabe_edit_valid_combox)



        # “预览”选项卡
        self.tab_preview = QWidget()
        self.tab_widget.addTab(self.tab_preview, '预览')

        tab_preview_layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.tab_preview.setLayout(tab_preview_layout)

        self.tab_preview_request_tittle = QLabel('请求模型', self.tab_preview)
        self.tab_preview_request_model = QTabWidget(self.tab_preview)
        self.tab_preview_response_tittle = QLabel('响应模型', self.tab_preview)
        self.tab_preview_response_model = QTabWidget(self.tab_preview)


        tab_preview_layout.addWidget(self.tab_preview_request_tittle)
        tab_preview_layout.addWidget(self.tab_preview_request_model)
        tab_preview_layout.addWidget(self.tab_preview_response_tittle)
        tab_preview_layout.addWidget(self.tab_preview_response_model)


        # 未选中时，禁用窗体
        # self.tab_widget.setEnabled(False)

    def fresh_data(self):
        """
        刷新数据
        """
        if self.main_window.curr_proj is not None:
            self.api_list_tree.fresh_proj(self.main_window.curr_proj)
            self.api_list_tree.fresh_data()

    def api_selected_event(self):
        pass
