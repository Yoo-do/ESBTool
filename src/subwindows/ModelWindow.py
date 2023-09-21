from PyQt5.QtWidgets import QWidget, QBoxLayout, QPushButton, QDialog

from src.widgets import ModelListWidgets, ModelDetailWidgets


class ModelWindow(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window

        self.ui_init()
        self.fresh_data()

    def ui_init(self):

        # 主布局，左右窗体
        main_layout = QBoxLayout(QBoxLayout.LeftToRight, self)

        self.model_list_tree = ModelListWidgets.ModelListTreeView(self, self.main_window.curr_proj)
        self.model_list_tree.clicked.connect(self.model_selected_event)
        self.model_list_tree.rewrite_signal.rewrite_signal.connect(self.clear_model_detail)
        main_layout.addWidget(self.model_list_tree)

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

        self.model_verify_button = QPushButton('校验json', self)
        self.model_verify_button.setEnabled(False)
        self.model_verify_button.clicked.connect(self.model_verify_event)
        model_detail_button_layout.addWidget(self.model_verify_button)

        self.model_save_button = QPushButton('保存', self)
        self.model_import_button.setEnabled(False)
        self.model_save_button.clicked.connect(self.model_save_event)
        model_detail_button_layout.addWidget(self.model_save_button)

        # 模型节点展示
        self.model_detial_tree = ModelDetailWidgets.ModelTreeView(self)

        model_detail_layout.addWidget(self.model_detial_tree)

        # 结构模型
        self.tree_standard_model: ModelDetailWidgets.ModelStandardModel = None

    def fresh_data(self):
        """
        刷新数据和全部数据窗体
        :return:
        """
        # 按钮状态调整
        self.model_import_button.setEnabled(False)
        self.model_verify_button.setEnabled(False)
        self.model_save_button.setEnabled(False)

        if self.tree_standard_model is not None:
            self.tree_standard_model.clear()

        if self.main_window.curr_proj is not None:
            self.model_list_tree.fresh_proj(self.main_window.curr_proj)
            self.model_list_tree.fresh_data()

        # 提示框删除
        self.main_window.clear_status_info()

    def clear_model_detail(self):
        self.model_import_button.setEnabled(False)
        self.model_verify_button.setEnabled(False)
        self.model_save_button.setEnabled(False)
        if self.tree_standard_model is not None:
            self.tree_standard_model.clear()

    def fresh_model_detail(self, data: dict):
        """
        刷新节点数据
        """
        if data is None:
            # 按钮状态调整
            self.clear_model_detail()
            return

        self.tree_standard_model = ModelDetailWidgets.ModelStandardModel()
        self.model_detial_tree.setModel(self.tree_standard_model)
        self.model_detial_tree.header().resizeSection(0, 300)

        self.generate_tree_model(self.tree_standard_model, data, '根节点')

    def generate_tree_model(self, parent, data, name='items'):
        try:

            # 生成节点
            root = ModelDetailWidgets.ModelStandardItem(self.model_detial_tree, parent, name, data.get('type'),
                                                        data.get('require'),
                                                        data.get('title'), data.get('description'))

            # 判断是否有子节点需要生成
            if data['type'] == 'object':
                if data.get('properties') is not None:
                    for key, value in data['properties'].items():
                        self.generate_tree_model(root, value, key)
            elif data['type'] == 'array':
                if data.get('items') is not None:
                    self.generate_tree_model(root, data.get('items'))
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

        index = self.model_list_tree.currentIndex()
        item = self.model_list_tree.model().itemFromIndex(index)

        if item.is_dir:
            # 文件夹的话则展开
            self.model_list_tree.expand(index)
            self.fresh_model_detail(None)
            return

        self.curr_model = self.main_window.curr_proj.get_model(item.get_full_name())
        data = self.curr_model.model

        self.fresh_model_detail(data)
        self.model_detial_tree.expandAll()

        # 更新按钮状态
        self.model_import_button.setEnabled(True)
        self.model_verify_button.setEnabled(True)
        self.model_save_button.setEnabled(True)

        self.main_window.show_status_info(f'已选中模型[{item.text()}]')

    def model_save_event(self):
        """保存事件"""
        self.curr_model.save(self.tree_standard_model.__jsonschema__())

        # 信息展示
        self.main_window.show_status_info(f'模型[{self.curr_model.model_name}]已保存')

    def model_import_event(self):
        """
        导入模型事件
        :return:
        """
        try:
            index = self.model_list_tree.currentIndex()
            item = self.model_list_tree.model().itemFromIndex(index)

            dialog = ModelDetailWidgets.ModelImportDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                curr_model = self.main_window.curr_proj.get_model(item.get_full_name())
                data = dialog.data
                curr_model.import_json(data)

                # 刷新节点
                self.model_selected_event()

        except Exception as e:
            print(e.__str__())

    def model_verify_event(self):
        index = self.model_list_tree.currentIndex()
        item = self.model_list_tree.model().itemFromIndex(index)
        curr_model = self.main_window.curr_proj.get_model(item.get_full_name())

        dialog = ModelDetailWidgets.ModelVerifyDialog(curr_model)
        dialog.exec_()
