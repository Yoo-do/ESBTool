from PyQt5.QtWidgets import QWidget, QStackedWidget, QBoxLayout, QLabel, QPushButton, \
    QDialog
from enum import Enum


from src.utils import Data
from src.subwindows import ModelWindow, IndexWindow, ApiWindow
from src.widgets import ModelListWidgets, CommonWidgets, ModelDetailWidgets


class SubWindowType(Enum):
    """
    全部子窗口类型
    """
    # 主页
    INDEX_WINDOW = 0,
    # 模型页面
    MODEL_WINDOW = 1,
    # 校验页面
    API_WINDOW = 2,









class SubWindow:
    """
    子窗口管理类
    """

    def __init__(self, main_window):
        self.main_window = main_window
        self.stack_widget = QStackedWidget(main_window)
        main_window.setCentralWidget(self.stack_widget)

        # 主页窗体
        self.stack_widget.addWidget(IndexWindow.IndexWindow(main_window))

        self.stack_widget.addWidget(ModelWindow.ModelWindow(main_window))

        self.stack_widget.addWidget(ApiWindow.ApiWindow(main_window))

    def switch_to_window(self, target_window_type: SubWindowType):
        self.stack_widget.setCurrentIndex(target_window_type.value[0])

        # 主页需要刷新数据
        if target_window_type == SubWindowType.INDEX_WINDOW:
            self.stack_widget.currentWidget().fresh_data()

    def fresh_all_data(self):
        for index in range(self.stack_widget.count()):
            widget = self.stack_widget.widget(index)
            widget.fresh_data()
