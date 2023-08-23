from PyQt5.QtWidgets import QApplication, QTreeView, QComboBox, QStyledItemDelegate, QItemEditorFactory, QItemEditorCreatorBase
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

class ComboBoxDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.addItems(['Option 1', 'Option 2', 'Option 3'])
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, role=Qt.DisplayRole)
        editor.setCurrentText(value)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, role=Qt.EditRole)

if __name__ == '__main__':
    app = QApplication([])

    # 创建一个QStandardItemModel对象
    model = QStandardItemModel()

    # 创建一些QStandardItem对象，并将其添加到模型中
    item1 = QStandardItem('Item 1')
    item2 = QStandardItem('Option 2')
    item3 = QStandardItem('Item 3')
    model.appendRow([item1, item2, item3])

    # 创建一个QTreeView对象，并将模型设置为其数据源
    tree_view = QTreeView()
    tree_view.setModel(model)

    # 将第二列的编辑器设置为QComboBox
    combo_box_delegate = ComboBoxDelegate()
    tree_view.setItemDelegateForColumn(1, combo_box_delegate)

    # 允许编辑
    tree_view.setEditTriggers(QTreeView.AllEditTriggers)

    # 显示窗口
    tree_view.show()

    app.exec_()