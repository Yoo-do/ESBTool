from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon,QBrush,QColor
import sys

class treeevent(QMainWindow):
    def __init__(self):
        super(treeevent,self).__init__()

        self.setWindowTitle("树控件的基本用法")
        self.resize(800,300)

        #创建树控件，设置列数为2
        self.tree=QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["key","value"])

        root=QTreeWidgetItem(self.tree)
        root.setText(0,"root")
        root.setText(1,"1")

        c1=QTreeWidgetItem(root)
        c1.setText(0,"child1")
        c1.setText(1,"2")

        c2=QTreeWidgetItem(c1)
        c2.setText(0,"child2")
        c2.setText(1,"3")
        c3 = QTreeWidgetItem(c1)
        c3.setText(0, "child3")
        c3.setText(1, "4")

 #为树节点设置信号与槽函数
        self.tree.clicked.connect(self.ontreeclick)
        self.setCentralWidget(self.tree)

    def ontreeclick(self,index):
        i=self.tree.currentItem()
        print(index.row())
        print('key=%s,value=%s' %(i.text(0),i.text(1)))

if __name__=="__main__":
    app=QApplication(sys.argv)
    p=treeevent()
    p.show()
    sys.exit(app.exec_())