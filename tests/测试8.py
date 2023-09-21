import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenuBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('设置选中状态')

        # 创建一个菜单栏
        menu_bar = self.menuBar()

        # 创建一个菜单
        menu = menu_bar.addMenu('菜单')

        # 创建一个动作
        action = QAction('动作', self)

        # 将动作添加到菜单中
        menu.addAction(action)

        # 设置动作的选中状态
        action.setChecked(True)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())