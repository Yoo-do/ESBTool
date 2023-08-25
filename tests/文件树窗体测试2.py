from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon,QBrush,QColor
import sys

class treechange(QWidget):
    def __init__(self):
        super(treechange,self).__init__()

        self.setWindowTitle("test")
        self.resize(800,300)

        layout=QHBoxLayout()
        add=QPushButton("添加节点")
        update=QPushButton("修改节点")
        delete=QPushButton("删除节点")

        layout.addWidget(add)
        layout.addWidget(update)
        layout.addWidget(delete)

        add.clicked.connect(self.add1)
        update.clicked.connect(self.update1)
        delete.clicked.connect(self.delete1)

  # 创建树控件，设置列数为2
        self.tree = QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["key", "value"])

        root = QTreeWidgetItem(self.tree)
        root.setText(0, "root")
        root.setText(1, "1")

        c1 = QTreeWidgetItem(root)
        c1.setText(0, "child1")
        c1.setText(1, "2")

        c2 = QTreeWidgetItem(c1)
        c2.setText(0, "child2")
        c2.setText(1, "3")
        c3 = QTreeWidgetItem(c1)
        c3.setText(0, "child3")
        c3.setText(1, "4")
        # 为树节点设置信号与槽函数
        self.tree.clicked.connect(self.ontreeclick)

        layout1=QVBoxLayout(self)
        layout1.addLayout(layout)
        layout1.addWidget(self.tree)
        self.setLayout(layout1)

    #显示的系统的根目录
        # model = QDirModel()  # 当前的系统model
        # tree = QTreeView()
        # tree.setModel(model)
        # tree.setWindowTitle("QTreeView控件与系统控件")
        # tree.resize(800, 1000)
        # layout1.addWidget(tree)

    def ontreeclick(self, index):
        i = self.tree.currentItem()
        print(index.row())
        print('key=%s,value=%s' % (i.text(0), i.text(1)))

#添加树节点
    def add1(self):
        print("添加节点")
        i=self.tree.currentItem()  #获取当前节点
        print(i)
        node=QTreeWidgetItem(i)   #为当前节点增加节点
        node.setText(0,"新节点")
        node.setText(1,"信值")

#修改节点
    def update1(self):
        print("修改节点")
        node= self.tree.currentItem()  # 获取当前节点
        node.setText(0, "修改节点")
        node.setText(1, "节点值已修改")

#删除节点
    def delete1(self):
        print("删除节点")
        node = self.tree.currentItem()  # 获取当前节点
        root=self.tree.invisibleRootItem()  #根是不可见的，所以需要另外出来进行删除
        if node in self.tree.selectedItems():
            (node.parent() or root).removeChild(node)

if __name__=="__main__":
    app=QApplication(sys.argv)
    p=treechange()
    p.show()
    sys.exit(app.exec_())