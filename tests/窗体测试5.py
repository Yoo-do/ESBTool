from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class tabwidgetDemo(QTabWidget):
    def __init__(self):
        super(tabwidgetDemo,self).__init__()

        self.setWindowTitle("选项卡控件QTabWidget")
        self.resize(800,300)

 #创建用于显示控件的窗口
        self.tab1=QWidget()
        self.tab2=QWidget()
        self.tab3=QWidget()

        self.addTab(self.tab1,"选项卡1")
        self.addTab(self.tab2, "选项卡2")
        self.addTab(self.tab3, "选项卡3")

        self.tab1UI()  #初始化第一个选项卡显示页面
        self.tab2UI()
        self.tab3UI()

 #第一个选项卡的页面设置
    def tab1UI(self):
        layout=QFormLayout()
        layout.addRow("姓名", QLineEdit())
        layout.addRow("地址",QLineEdit())
        self.setTabText(0,"联系方式")  #设置第一个选项卡的标题为联系方式
        self.tab1.setLayout(layout)

    def tab2UI(self):
        layout1=QFormLayout()
        sex=QHBoxLayout()
        sex.addWidget(QRadioButton("男"))
        sex.addWidget(QRadioButton("女"))
        layout1.addRow(QLabel("性别"),sex)
        layout1.addRow("生日",QLineEdit())
        self.setTabText(1,"个人详细信息")
        self.tab2.setLayout(layout1)

    def tab3UI(self):
        layout2=QHBoxLayout()
        layout2.addWidget(QLabel("科目"))
        layout2.addWidget(QCheckBox("物理"))
        layout2.addWidget(QCheckBox("高数"))
        self.setTabText(2,"教育程度")
        self.tab3.setLayout(layout2)

if __name__=="__main__":
    app=QApplication(sys.argv)
    p=tabwidgetDemo()
    p.show()
    sys.exit(app.exec_())