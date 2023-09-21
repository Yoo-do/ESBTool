from PyQt5.QtWidgets import QWidget, QBoxLayout, QLabel, QPushButton, QDialog, QFormLayout, QLineEdit
class IndexWindow(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window

        self.ui_init()
        self.fresh_data()

    def ui_init(self):

        # 主布局
        main_layout = QBoxLayout(QBoxLayout.TopToBottom, self)
        main_layout.setContentsMargins(100, 100, 100, 100)
        main_layout.setSpacing(50)


        # 信息展示表单
        self.info_form = QFormLayout(self)
        main_layout.addLayout(self.info_form)

        # 项目名称
        self.proj_name_title = QLabel('项目名称: ')
        self.proj_name_title_lineedit = QLineEdit()
        self.proj_name_title_lineedit.setDisabled(True)
        self.info_form.addRow(self.proj_name_title, self.proj_name_title_lineedit)

        # 模型数量
        self.model_nums_title = QLabel('模型数量: ')
        self.model_nums_title_lineedit = QLineEdit()
        self.model_nums_title_lineedit.setDisabled(True)
        self.info_form.addRow(self.model_nums_title, self.model_nums_title_lineedit)

        # 接口数量
        self.api_nums_title = QLabel('接口数量: ')
        self.api_nums_title_lineedit = QLineEdit()
        self.api_nums_title_lineedit.setDisabled(True)
        self.info_form.addRow(self.api_nums_title, self.api_nums_title_lineedit)


    def clear_data(self):
        """
        清空数据
        """
        self.proj_name_title_lineedit.clear()
        self.model_nums_title_lineedit.clear()
        self.api_nums_title_lineedit.clear()

    def fresh_data(self):
        self.clear_data()

        if self.main_window.curr_proj_name is None:
            self.proj_name_title_lineedit.setText('未选择项目')
            return


        self.proj_name_title_lineedit.setText(self.main_window.curr_proj_name)
        self.model_nums_title_lineedit.setText(self.main_window.curr_proj.get_model_nums().__str__())
        self.api_nums_title_lineedit.setText(self.main_window.curr_proj.get_api_nums().__str__())