from PyQt5.QtWidgets import QWidget, QBoxLayout, QLabel, QPushButton, QDialog


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
        pass

    def fresh_data(self):
        """
        刷新数据
        """
        pass
