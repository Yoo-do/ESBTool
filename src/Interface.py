"""
全部的窗体类
"""

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QInputDialog, QMessageBox, QFileDialog, QMenu
from PyQt5.Qt import Qt, QThread, pyqtSignal, QIcon, QPixmap
import sys
import path_lead

from utils import FileIO


class Interface(QMainWindow):
    """
    主界面类
    """

    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()
        self.ui_init()

        sys.exit(self.app.exec_())

    def ui_init(self):
        """
        ui初始化
        :return:
        """

        self.resize(1000, 800)
        self.move(400, 100)
        self.window_tittle = 'ESBTool 测试版'
        self.setWindowTitle(self.window_tittle)
        self.setWindowIcon(QIcon(QPixmap(path_lead.get_path(r'\icon\ESBTool.png'))))

        # 菜单栏初始化
        self.menubar_init()

        self.show()

    def menubar_init(self):
        """
        菜单初始化
        :return:
        """

        self.menubar = QMenuBar()
        self.menubar.show()
        self.setMenuBar(self.menubar)

        # 项目菜单栏
        self.proj_menu = QMenu('项目', self)
        self.open_proj_action = QAction('打开项目')
        self.proj_menu.addAction(self.open_proj_action)

        self.add_proj_action = QAction('新增项目')
        self.add_proj_action.triggered.connect(self.add_proj_event)
        self.proj_menu.addAction(self.add_proj_action)
        self.menubar.addMenu(self.proj_menu)

        # 事件设置
        self.index_action = QAction('主页')
        self.menubar.addAction(self.index_action)
        self.index_action.triggered.connect(self.show_index_window)

        self.model_action = QAction('模型')
        self.menubar.addAction(self.model_action)
        self.model_action.triggered.connect(self.show_model_window)

    """事件"""

    def add_proj_event(self):
        """
        新增项目事件
        """
        try:
            proj_name, ok = QInputDialog.getText(self, '新增项目', '项目名称')
            if ok:
                FileIO.ProjIO.add_proj(proj_name)

        except Exception as e:
            QMessageBox.critical(self, '错误消息', e.__str__(), QMessageBox.Ok)

    def show_index_window(self):
        pass

    def show_model_window(self):
        pass


if __name__ == '__main__':
    interface = Interface()
