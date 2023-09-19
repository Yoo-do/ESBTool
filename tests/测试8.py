from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget

# 自定义信号类
class MySignal(QObject):
    my_signal = pyqtSignal()  # 定义一个信号

# 继承QTreeView的自定义类
class MyTreeView(QTreeView):
    def __init__(self):
        super().__init__()
        self.my_signal = MySignal()  # 实例化自定义信号类

    def do_something(self):
        # 执行某个方法
        # ...

        self.my_signal.my_signal.emit()  # 发出信号

# 主窗体类
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tree_view = MyTreeView()
        self.setCentralWidget(self.tree_view)

        self.tree_view.my_signal.my_signal.connect(self.special_method)  # 连接信号与槽

    def special_method(self):
        # 执行特定方法
        # ...
        print("收到信号，执行特定方法")

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()