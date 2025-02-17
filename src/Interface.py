"""
全部的窗体类
"""
import logging

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QInputDialog, QMessageBox, QMenu, QDialog
from PyQt5.Qt import QIcon, QPixmap
import sys
import path_lead

from src.utils import FileIO, Data, Log
from src.subwindows import SubWindow
from src.widgets import CommonWidgets


class Interface(QMainWindow):
    """
    主界面类
    """

    def __init__(self):
        self.app = QApplication(sys.argv)
        try:
            super().__init__()

            self.proj_init()
            self.sub_window_object = SubWindow.SubWindow(self)
            self.ui_init()

        except Exception as e:
            QMessageBox.critical(self, '错误消息', e.__str__())

        sys.exit(self.app.exec_())

    def ui_init(self):
        """
        ui初始化
        :return:
        """

        self.resize(1000, 800)
        self.move(400, 100)
        self.window_title = 'ESBTool 测试版'
        self.setWindowTitle(self.window_title)
        self.setWindowIcon(QIcon(QPixmap(path_lead.get_path(r'\icon\ESBTool.png'))))

        # 菜单栏初始化
        self.menubar_init()

        self.show_index_window()

        self.show()

        Log.logger.info('主界面初始化完成')

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
        self.open_proj_action.triggered.connect(self.open_proj_event)
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

        self.api_action = QAction('接口')
        self.menubar.addAction(self.api_action)
        self.api_action.triggered.connect(self.show_api_window)

        self.test_action = QAction('测试')
        self.menubar.addAction(self.test_action)
        self.test_action.triggered.connect(self.test_event)

        self.set_actions_enable(False)

    def proj_init(self):
        """
        初始化项目
        """
        self.curr_proj_name = None
        self.curr_proj = None

    def set_current_proj(self, proj_name):
        """
        切换项目
        """
        self.curr_proj_name = proj_name
        if proj_name is not None:
            self.curr_proj_name = proj_name
            self.curr_proj = Data.Proj(proj_name)
            self.setWindowTitle(self.window_title + '  -- ' + proj_name)

            self.set_actions_enable(True)

    def set_actions_enable(self, a0: bool):
        """
        控制按钮是否可用
        """
        self.model_action.setEnabled(a0)
        self.api_action.setEnabled(a0)

    def show_status_info(self, info: str):
        """
        展示提示消息
        """
        self.statusBar().showMessage(info)

    def clear_status_info(self):
        """
        清除提示消息
        """
        self.setStatusTip('')

        # 日志
        logging.debug('清除了status信息')

    """事件"""

    def open_proj_event(self):
        proj_names = FileIO.ProjIO.get_proj_names()
        dialog = CommonWidgets.ProjListDialog(self, '选择项目', proj_names)
        if dialog.exec_() == QDialog.Accepted:
            selected_proj = [item.text() for item in dialog.list_widget.selectedItems()][0]
            self.set_current_proj(selected_proj)

            # 切换项目的时候刷新全部窗体数据，并切换到到主页
            self.sub_window_object.fresh_all_data()
            self.show_index_window()

            # 日志
            Log.logger.info(f'打开项目[{selected_proj}]')

    def add_proj_event(self):
        """
        新增项目事件
        """
        try:
            proj_name, ok = QInputDialog.getText(self, '新增项目', '项目名称')
            if ok:
                FileIO.ProjIO.add_proj(proj_name)

                # 日志
                Log.logger.info(f'新增项目[{proj_name}]')


                # 打开该项目
                self.set_current_proj(proj_name)
                self.sub_window_object.fresh_all_data()
                self.show_index_window()


        except Exception as e:
            QMessageBox.critical(self, '错误消息', e.__str__(), QMessageBox.Ok)

    def switch_menubar_action(self, action: QAction):
        """
        高亮当前窗口
        """
        self.index_action.setChecked(False)
        self.model_action.setChecked(False)
        self.api_action.setChecked(False)

        action.setChecked(True)

    def show_index_window(self):
        self.switch_menubar_action(self.index_action)
        self.sub_window_object.switch_to_window(SubWindow.SubWindowType.INDEX_WINDOW)

    def show_model_window(self):
        self.switch_menubar_action(self.model_action)
        self.sub_window_object.switch_to_window(SubWindow.SubWindowType.MODEL_WINDOW)

    def show_api_window(self):
        self.switch_menubar_action(self.api_action)
        self.sub_window_object.switch_to_window(SubWindow.SubWindowType.API_WINDOW)

    def test_event(self):
        """
        测试事件
        """
        pass


if __name__ == '__main__':
    interface = Interface()
