from PyQt5.QtWidgets import QWidget, QBoxLayout, QLabel, QPushButton, QDialog, QTabWidget, QComboBox, QTextEdit, QLineEdit
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
        self.tab_edit_url_tittle = QLabel('url', self.tab_edit)
        self.tab_edit_url_editline = QLineEdit(self.tab_edit)
        self.tab_edit_request_tittle = QLabel('请求模型', self.tab_edit)
        self.tab_edit_request_combox = QComboBox(self.tab_edit)
        self.tab_edit_response_tittle = QLabel('响应模型', self.tab_edit)
        self.tab_edit_response_combox = QComboBox(self.tab_edit)
        self.tab_edit_description_tittle = QLabel('描述信息', self.tab_edit)
        self.tab_edit_description_textedit = QTextEdit(self.tab_edit)
        self.tab_edit_description_textedit.adjustSize()
        self.tab_edit_valid_tittle = QLabel('是否废弃', self.tab_edit)
        self.tab_edit_valid_combox = QComboBox(self.tab_edit)

        tab_edit_layout.addWidget(self.tab_edit_url_tittle)
        tab_edit_layout.addWidget(self.tab_edit_url_editline)
        tab_edit_layout.addWidget(self.tab_edit_request_tittle)
        tab_edit_layout.addWidget(self.tab_edit_request_combox)
        tab_edit_layout.addWidget(self.tab_edit_response_tittle)
        tab_edit_layout.addWidget(self.tab_edit_response_combox)
        tab_edit_layout.addWidget(self.tab_edit_description_tittle)
        tab_edit_layout.addWidget(self.tab_edit_description_textedit)
        tab_edit_layout.addWidget(self.tab_edit_valid_tittle)
        tab_edit_layout.addWidget(self.tab_edit_valid_combox)



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

    def disable_tab_widget(self):
        """
        选项卡数据清空并禁用
        :return:
        """
        self.edit_tab_clear_data()
        self.preview_tab_clear_data()

        self.tab_widget.setCurrentIndex(0)
        self.tab_widget.setEnabled(False)


    def fresh_data(self):
        """
        刷新数据
        """
        if self.main_window.curr_proj is not None:
            self.api_list_tree.fresh_proj(self.main_window.curr_proj)
            self.api_list_tree.fresh_data()


        self.disable_tab_widget()

    def edit_tab_clear_data(self):
        """
        设置选项卡清空数据
        :return:
        """
        if not self.tab_widget.isEnabled():
            return

        self.tab_edit_request_combox.clear()
        self.tab_edit_response_combox.clear()
        self.tab_edit_description_textedit.clear()
        self.tab_edit_valid_combox.clear()

    def edit_tab_fresh_data(self):
        """
        设置选项卡数据刷新
        :return:
        """
        if not self.tab_widget.isEnabled():
            return

        url = self.curr_api.get_url()
        self.tab_edit_url_editline.setText(url)


        # 请求模型
        request_name = self.curr_api.get_request_name()
        request_path = self.curr_api.get_request_name()
        self.request_models = self.main_window.curr_proj.get_all_model_name_path()
        if {'name': request_name, 'path': request_path} not in self.request_models:
            self.request_models.append({'name': request_name, 'path': request_path})

        self.tab_edit_request_combox.addItems([item.get('name') for item in self.request_models])
        self.tab_edit_request_combox.setCurrentText(request_name)

        # 响应模型
        response_name = self.curr_api.get_response_name()
        response_path = self.curr_api.get_response_name()
        self.response_models = self.main_window.curr_proj.get_all_model_name_path()
        if {'name': response_name, 'path': response_path} not in self.response_models:
            self.response_models.append({'name': response_name, 'path': response_path})

        self.tab_edit_response_combox.addItems([item.get('name') for item in self.response_models])
        self.tab_edit_response_combox.setCurrentText(response_name)



    def preview_tab_clear_data(self):
        """
        预览选项卡清空数据
        :return:
        """
        if not self.tab_widget.isEnabled():
            return

        self.tab_preview_request_model.clear()
        self.tab_preview_response_model.clear()




    def preview_tab_fresh_data(self):
        """
        预览选项卡数据刷新
        :return:
        """
        pass

    def api_selected_event(self):
        index = self.api_list_tree.currentIndex()
        item = self.api_list_tree.model().itemFromIndex(index)

        if item.is_dir:
            # 文件夹的话则展开
            self.api_list_tree.expand(index)
            self.disable_tab_widget()
            return

        # 当前api
        self.curr_api = self.main_window.curr_proj.get_api(item.get_full_name())
        self.tab_widget.setEnabled(True)
        self.edit_tab_fresh_data()
        self.preview_tab_fresh_data()