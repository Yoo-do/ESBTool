from PyQt5.QtWidgets import QApplication, QDialog, QListWidget, QVBoxLayout, QDialogButtonBox


class ListDialog(QDialog):
    def __init__(self, items):
        super().__init__()

        self.setWindowTitle("List Dialog")

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.addItems(items)
        layout.addWidget(self.list_widget)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)


# 使用示例
if __name__ == "__main__":
    app = QApplication([])

    items = ["Item 1", "Item 2", "Item 3", "Item 4"]

    dialog = ListDialog(items)
    if dialog.exec_() == QDialog.Accepted:
        selected_items = [item.text() for item in dialog.list_widget.selectedItems()]
        print("Selected items:", selected_items)

    app.exec_()