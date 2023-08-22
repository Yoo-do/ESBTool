from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

if __name__=="__main__":
    app=QApplication(sys.argv)

 #显示当前的系统根目录的列表
    model=QDirModel()  #当前的系统model
    tree=QTreeView()
    tree.setModel(model)
    tree.setWindowTitle("QTreeView控件与系统控件")
    tree.resize(800,1000)
    tree.show()
    sys.exit(app.exec_())