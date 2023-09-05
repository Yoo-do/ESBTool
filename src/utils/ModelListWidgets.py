from PyQt5.QtWidgets import QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from src.utils import FileIO

class ModelListStandardItem(QStandardItem):
    def __init__(self, parent: QStandardItemModel | QStandardItem, name: str, is_dir: bool, real_path: str):
        super().__init__(name)
        self.is_dir = is_dir
        self.real_path = real_path
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


    def generate_model(self):
        pass
