from PyQt5.QtWidgets import QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from src.utils import FileIO

class ModelListStandardItem(QStandardItem):
    def __init__(self, parent: QStandardItemModel | QStandardItem, name: str, is_dir: bool, path: str=None):
        super().__init__(name)
        self.is_dir = is_dir
        self.path = path
        parent.appendRow(self)


class ModelListStandardModel(QStandardItemModel):
    def __init__(self):
        super().__init__()
        self.headers = ['名称']
        self.setHorizontalHeaderLabels(self.headers)


class ModelListTreeView(QTreeView):
    def __init__(self, parent):
        super().__init__(parent)

    def fresh_data(self, proj):
        proj.fresh_model_config()
        model_config = proj.model_config

        model = ModelListStandardModel()

        self.generate_model(model, model_config)

        self.setModel(model)


    def generate_model(self, parent, data: list):
        for item in data:
            root = ModelListStandardItem(parent, item.get('name'), item.get('is_dir'), item.get('path'))
            if item.get('is_dir'):
                self.generate_model(root, item.get('items'))

