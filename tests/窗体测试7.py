from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys


class dockwidgetDemo(QMainWindow):
    def __init__(self):
        super(dockwidgetDemo, self).__init__()

        self.setWindowTitle("停靠控件QDockWidget")
        self.resize(1000, 800)

        layout=QHBoxLayout()
        self.dock=QDockWidget("Dockable",self)
        self.listwidget=QListWidget()
        self.listwidget.addItem("item1")
        self.listwidget.addItem("item2")
        self.listwidget.addItem("item3")

        self.dock.setWidget(self.listwidget)
        self.setCentralWidget(QTextEdit("编辑器"))

#设置默认停靠在右边
        self.addDockWidget(Qt.RightDockWidgetArea,self.dock)
        self.dock.setFloating(True)   #使其处于悬浮状态
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    p = dockwidgetDemo()
    p.show()
    sys.exit(app.exec_())