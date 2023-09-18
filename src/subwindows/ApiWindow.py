from PyQt5.QtWidgets import QWidget, QBoxLayout, QLabel, QPushButton, QDialog, QTabWidget, QComboBox, QTextEdit, \
    QLineEdit, QTableView, QAbstractItemView, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from src.widgets import ApiListWidgets
from src.utils import Log


class ApiWindow(QWidget):
    """
    接口层窗口
    """

    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window

        self.request_table_model: QStandardItemModel = None
        self.response_table_model: QStandardItemModel = None

        self.is_connect = False
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
        self.tab_edit_valid_tittle = QLabel('是否在用', self.tab_edit)
        self.tab_edit_valid_combox = QComboBox(self.tab_edit)


        # 布局
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
        self.tab_preview_request_model_table = QTableView(self.tab_preview)
        self.tab_preview_request_model_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tab_preview_response_tittle = QLabel('响应模型', self.tab_preview)
        self.tab_preview_response_model_table = QTableView(self.tab_preview)
        self.tab_preview_response_model_table.setEditTriggers(QAbstractItemView.NoEditTriggers)


        # 窗体放入布局
        tab_preview_layout.addWidget(self.tab_preview_request_tittle)
        tab_preview_layout.addWidget(self.tab_preview_request_model_table)
        tab_preview_layout.addWidget(self.tab_preview_response_tittle)
        tab_preview_layout.addWidget(self.tab_preview_response_model_table)

        # 未选中时，禁用窗体
        self.tab_widget.setEnabled(False)

    def disable_tab_widget(self):
        """
        选项卡数据清空并禁用
        :return:
        """
        if self.tab_widget.isEnabled():
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

        # 解绑
        if self.is_connect:
            self.tab_edit_url_editline.textChanged.disconnect(self.url_changed)
            self.tab_edit_request_combox.currentTextChanged.disconnect(self.request_combox_changed)
            self.tab_edit_response_combox.currentTextChanged.disconnect(self.response_combox_changed)
            self.tab_edit_description_textedit.textChanged.disconnect(self.description_changed)
            self.tab_edit_valid_combox.currentTextChanged.disconnect(self.valid_changed)
            self.is_connect = False

        self.tab_edit_url_editline.clear()
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

        self.edit_tab_clear_data()

        url = self.curr_api.get_url()
        self.tab_edit_url_editline.setText(url)


        # 请求模型
        request_name = self.curr_api.get_request_name()
        request_path = self.curr_api.get_request_name()
        self.request_models = self.main_window.curr_proj.get_all_model_name_path()
        if request_name not in [item.get('name') for item in self.request_models]:
            self.request_models.append({'name': request_name, 'path': request_path})

        self.tab_edit_request_combox.addItems([item.get('name') for item in self.request_models])
        self.tab_edit_request_combox.setCurrentText(request_name)

        # 响应模型
        response_name = self.curr_api.get_response_name()
        response_path = self.curr_api.get_response_name()
        self.response_models = self.main_window.curr_proj.get_all_model_name_path()
        if response_name not in [item.get('name') for item in self.response_models]:
            self.response_models.append({'name': response_name, 'path': response_path})

        self.tab_edit_response_combox.addItems([item.get('name') for item in self.response_models])
        self.tab_edit_response_combox.setCurrentText(response_name)

        # 描述
        description = self.curr_api.get_description()
        self.tab_edit_description_textedit.setText(description)

        # 是否有效
        valid = self.curr_api.get_valid()
        self.tab_edit_valid_combox.addItems(['是', '否'])
        if valid:
            self.tab_edit_valid_combox.setCurrentIndex(0)
        else:
            self.tab_edit_valid_combox.setCurrentIndex(1)

        # 绑定事件
        if not self.is_connect:
            self.tab_edit_url_editline.textChanged.connect(self.url_changed)
            self.tab_edit_request_combox.currentTextChanged.connect(self.request_combox_changed)
            self.tab_edit_response_combox.currentTextChanged.connect(self.response_combox_changed)
            self.tab_edit_description_textedit.textChanged.connect(self.description_changed)
            self.tab_edit_valid_combox.currentTextChanged.connect(self.valid_changed)
            self.is_connect = True

    def preview_tab_clear_data(self):
        """
        预览选项卡清空数据
        :return:
        """
        if not self.tab_widget.isEnabled():
            return
        if self.request_table_model is not None:
            self.request_table_model.clear()

        if self.response_table_model is not None:
            self.response_table_model.clear()

    def preview_tab_fresh_data(self):
        """
        预览选项卡数据刷新
        :return:
        """

        self.preview_tab_clear_data()

        models = self.main_window.curr_proj.get_all_model_name_path()

        # 分别获取请求响应的模型path
        request_path = self.curr_api.get_request_path()
        if request_path in [model.get('path') for model in models]:
            request_data = self.main_window.curr_proj.get_model_data(request_path)

            self.request_table_model = QStandardItemModel(self.tab_preview_request_model_table)
            self.request_table_model.setHorizontalHeaderLabels(['节点', '类型', '必选', '中文名', '描述'])

            self.tab_preview_request_model_table.setModel(self.request_table_model)
            self.generate_request_table(request_data.get('properties'))

            # 自适应大小
            self.tab_preview_request_model_table.resizeColumnsToContents()
            self.tab_preview_request_model_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        response_path = self.curr_api.get_response_path()
        if response_path in [model.get('path') for model in models]:
            response_data = self.main_window.curr_proj.get_model_data(response_path)

            self.response_table_model = QStandardItemModel(self.tab_preview_response_model_table)
            self.response_table_model.setHorizontalHeaderLabels(['节点', '类型', '必选', '中文名', '描述'])

            self.tab_preview_response_model_table.setModel(self.response_table_model)
            self.generate_response_table(response_data.get('properties'))

            # 自适应大小
            self.tab_preview_response_model_table.resizeColumnsToContents()
            self.tab_preview_response_model_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


    def generate_request_table(self, data: dict):
        """
        请求预览生成
        """
        if data is None:
            return

        for key, value in data.items():
            name_item = QStandardItem(key)
            type_item = QStandardItem(value.get('type'))
            required_item = QStandardItem('是' if value.get('require') else '否')
            tittle_item = QStandardItem(value.get('tittle'))
            description_item = QStandardItem(value.get('description'))

            self.request_table_model.appendRow([name_item, type_item, required_item, tittle_item, description_item])

            data_type = value.get('type')
            if data_type == 'object':
                self.generate_request_table(value.get('properties'))
            elif data_type == 'array':
                self.generate_request_table(value.get('items').get('properties'))
    def generate_response_table(self, data: dict):
        """
        响应预览生成
        """
        if data is None:
            return

        for key, value in data.items():
            name_item = QStandardItem(key)
            type_item = QStandardItem(value.get('type'))
            required_item = QStandardItem('是' if value.get('require') else '否')
            tittle_item = QStandardItem(value.get('tittle'))
            description_item = QStandardItem(value.get('description'))

            self.response_table_model.appendRow([name_item, type_item, required_item, tittle_item, description_item])

            data_type = value.get('type')
            if data_type == 'object':
                self.generate_response_table(value.get('properties'))
            elif data_type == 'array':
                self.generate_response_table(value.get('items').get('properties'))








    # 响应事件
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

    def request_combox_changed(self):
        """
        请求模型修改
        :return:
        """
        index = self.tab_edit_request_combox.currentIndex()
        request_name = self.request_models[index].get('name')
        request_path = self.request_models[index].get('path')

        self.curr_api.set_request_name(request_name)
        self.curr_api.set_request_path(request_path)

        Log.logger.info(f'接口 [{self.curr_api.api_name}] 的请求模型修改为 [{request_name}]')

    def response_combox_changed(self):
        """
        响应模型修改
        :return:
        """
        index = self.tab_edit_response_combox.currentIndex()
        response_name = self.response_models[index].get('name')
        response_path = self.response_models[index].get('path')

        self.curr_api.set_response_name(response_name)
        self.curr_api.set_response_path(response_path)

        Log.logger.info(f'接口 [{self.curr_api.api_name}] 的响应模型修改为 [{response_name}]')

    def description_changed(self):
        """
        描述修改
        :return:
        """
        description = self.tab_edit_description_textedit.toPlainText()
        self.curr_api.set_description(description)

        Log.logger.info(f'接口 [{self.curr_api.api_name}] 的描述修改为 [{description}]')

    def url_changed(self):
        """
        url修改
        :return:
        """
        url = self.tab_edit_url_editline.text()
        self.curr_api.set_url(url)

        Log.logger.info(f'接口 [{self.curr_api.api_name}] 的url修改为 [{url}]')

    def valid_changed(self):
        """
        valid修改
        :return:
        """
        valid = True if self.tab_edit_valid_combox.currentText() == '是' else False
        self.curr_api.set_valid(valid)

        Log.logger.info(f'接口 [{self.curr_api.api_name}] 的valid修改为 [{valid}]')
