from PyQt5.QtWidgets import QWidget, QBoxLayout, QLabel, QPushButton, QDialog, QTabWidget

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


        # “预览”选项卡
        self.tab_preview = QWidget()
        self.tab_widget.addTab(self.tab_preview, '预览')

    def fresh_data(self):
        """
        刷新数据
        """
        if self.main_window.curr_proj is not None:
            self.api_list_tree.fresh_proj(self.main_window.curr_proj)
            self.api_list_tree.fresh_data()

    def api_selected_event(self):
        pass
