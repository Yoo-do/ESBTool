from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QBrush,QColor
import sys

class treewidget(QMainWindow):
    def __init__(self):
        super(treewidget,self).__init__()

        self.setWindowTitle("树控件的基本用法")
        self.resize(800,300)

#设置树控件
        self.tree=QTreeWidget()
        self.tree.setColumnCount(2) #制定树控件为两列
        self.tree.setHeaderLabels(["key","value"]) #设置列标签

 #添加根节点1
        root=QTreeWidgetItem(self.tree)
        root.setText(0,"根节点")
        root.setIcon(0,QIcon("./image/1.png"))
        self.tree.setColumnWidth(0,300)

 #添加子节点1
        n1=QTreeWidgetItem(root)
        n1.setText(0,"子节点1")
        n1.setText(1,"子节点的数据")
        n1.setIcon(0,QIcon("./image/1.png"))
        n1.setCheckState(0,Qt.Checked)  #添加复选框
        #添加子节点2
        n2=QTreeWidgetItem(root)
        n2.setText(0, "子节点2")
        n2.setText(1, "子节点2的数据")
        n2.setIcon(0, QIcon("./image/1.png"))
        n2.setCheckState(0, Qt.Checked)  # 添加复选框

#为子节点再添加子节点2-1
        n3 = QTreeWidgetItem(n2)
        n3.setText(0, "子节点2-1")
        n3.setText(1, "子节点2-1的数据")
        n3.setIcon(0, QIcon("./image/1.png"))
        n3.setCheckState(0, Qt.Checked)  # 添加复选框

        self.tree.expandAll()  #设置所有的节点为展开的状态
        self.setCentralWidget(self.tree)

if __name__=="__main__":
    app=QApplication(sys.argv)
    p=treewidget()
    p.show()
    sys.exit(app.exec_())