import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel

class TabDemo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("选项卡示例")
        self.setGeometry(100, 100, 400, 300)

        # 创建一个选项卡控件
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        # 创建两个选项卡
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        # 将选项卡添加到选项卡控件中
        self.tab_widget.addTab(self.tab1, "选项卡1")
        self.tab_widget.addTab(self.tab2, "选项卡2")

        # 在第一个选项卡中添加一些内容
        layout1 = QVBoxLayout()
        label1 = QLabel("这是选项卡1的内容", self.tab1)
        layout1.addWidget(label1)
        self.tab1.setLayout(layout1)

        # 在第二个选项卡中添加一些内容
        layout2 = QVBoxLayout()
        label2 = QLabel("这是选项卡2的内容", self.tab2)
        layout2.addWidget(label2)
        self.tab2.setLayout(layout2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = TabDemo()
    demo.show()
    sys.exit(app.exec_())