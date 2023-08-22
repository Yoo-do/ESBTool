from PyQt5.QtWidgets import QWidget, QMainWindow, QStackedWidget, QBoxLayout, QLabel
from PyQt5.Qt import Qt, QThread, pyqtSignal
from enum import Enum
from src.utils import Data


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


class SubWindow:
    """
    子窗口管理类
    """

    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window
        self.stack_widget = QStackedWidget(main_window)
        main_window.setCentralWidget(self.stack_widget)

        self.stack_widget.addWidget(IndexWindow(main_window))

    def switch_to_window(self, target_window_type: SubWindowType):
        self.stack_widget.setCurrentIndex(target_window_type.value[0])

    def fresh_all_data(self):
        for index in range(self.stack_widget.count()):
            widget = self.stack_widget.widget(index)
            widget.fresh_data()
