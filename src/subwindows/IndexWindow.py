from PyQt5.QtWidgets import QWidget, QBoxLayout, QLabel, QPushButton, QDialog
class IndexWindow(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window

        self.ui_init()
        self.fresh_data()

    def ui_init(self):
        self.show()
        layout = QBoxLayout(QBoxLayout.TopToBottom, self)

        self.label = QLabel(self)
        self.label.show()
        layout.addWidget(self.label)

    def fresh_data(self):
        if self.main_window.curr_proj_name is None:
            self.label.setText('未选择项目')
        else:
            self.label.setText(self.main_window.curr_proj_name)