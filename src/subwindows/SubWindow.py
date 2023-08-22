from PyQt5.QtWidgets import QWidget, QMainWindow, QStackedWidget
from PyQt5.Qt import Qt, QThread, pyqtSignal
from enum import Enum


class SubWindowBase(QWidget):
    """
    子窗口基类
    """

    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window
        super().__init__(self.main_window)


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


class SubWindow:
    """
    子窗口管理类
    """

    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window
        self.stack_widget = QStackedWidget(main_window)
        main_window.setCentralWidget(self.stack_widget)
