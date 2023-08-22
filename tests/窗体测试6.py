from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class stackwidgetDemo(QTabWidget):
    def __init__(self):
        super(stackwidgetDemo,self).__init__()

        self.setWindowTitle("堆栈控件QStackWidget")
        self.resize(1000,800)

        self.list=QListWidget()
        self.list.insertItem(0,"联系信息")
        self.list.insertItem(1,"个人信息")
        self.list.insertItem(2,"教育程度")

        self.list.currentRowChanged.connect(self.display)
        self.stack1=QWidget()
        self.stack2=QWidget()
        self.stack3=QWidget()

        self.stack=QStackedWidget()
        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)

        hb=QHBoxLayout()
        hb.addWidget(self.list)
        hb.addWidget(self.stack)
        self.setLayout(hb)

    def display(self,index):
        self.stack.setCurrentIndex(index)

        self.tab1UI()  #初始化第一个选项卡显示页面
        self.tab2UI()
        self.tab3UI()

  #第一个选项卡的页面设置
    def tab1UI(self):
        layout=QFormLayout()
        layout.addRow("姓名", QLineEdit())
        layout.addRow("地址",QLineEdit())
        self.stack1.setLayout(layout)

    def tab2UI(self):
        layout1=QFormLayout()
        sex=QHBoxLayout()
        sex.addWidget(QRadioButton("男"))
        sex.addWidget(QRadioButton("女"))
        layout1.addRow(QLabel("性别"),sex)
        layout1.addRow("生日",QLineEdit())
        self.stack2.setLayout(layout1)

    def tab3UI(self):
        layout2=QHBoxLayout()
        layout2.addWidget(QLabel("科目"))
        layout2.addWidget(QCheckBox("物理"))
        layout2.addWidget(QCheckBox("高数"))
        self.stack3.setLayout(layout2)

if __name__=="__main__":
    app=QApplication(sys.argv)
    p=stackwidgetDemo()
    p.show()
    sys.exit(app.exec_())