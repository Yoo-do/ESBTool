"""

"""

from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QLineEdit, QSpinBox, QComboBox

app = QApplication([])

tree = QTreeWidget()
tree.setColumnCount(3)
tree.setHeaderLabels(['列1', '列2', '列3'])

# 创建一个可以直接编辑的小部件
def create_edit_widget(value):
    widget = QLineEdit()
    widget.setText(value)
    return widget

# 添加节点和子节点
root = QTreeWidgetItem(tree, ['节点1', '值1', '值2'])
child1 = QTreeWidgetItem(root, ['子节点1', '值3', '值4'])
child2 = QTreeWidgetItem(root, ['子节点2', '值5', '值6'])

# 将可编辑小部件设置为每个单元格的小部件
for column in range(tree.columnCount()):
    tree.setItemWidget(root, column, create_edit_widget(root.text(column)))
    tree.setItemWidget(child1, column, create_edit_widget(child1.text(column)))
    tree.setItemWidget(child2, column, create_edit_widget(child2.text(column)))

tree.show()
app.exec()