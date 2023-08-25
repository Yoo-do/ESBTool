"""
数据模型层，为前端窗体提供数据结构支持
"""

import json
import jsonschema
from src.utils import FileIO

ModelDataTypes = ['object', 'array', 'integer', 'number', 'string', 'boolean']


class Model:
    """
    数据模型类
    """
    def __init__(self, proj_name: str, model_name: str, model: dict):
        self.proj_name = proj_name
        self.model_name = model_name
        self.model = model

    def validate(self, data: dict) -> bool:
        try:
            jsonschema.validate(data, self.model)
            return True
        except jsonschema.ValidationError as e:
            raise Exception(e.path).__str__() + ' : ' + e.message.__str__()


    @staticmethod
    def generate_jsonschema(json_data):
        """生成jsonschema"""

        def get_type(data):
            if isinstance(data, dict):
                return 'object'
            elif isinstance(data, list):
                return 'array'
            elif isinstance(data, int):
                return 'integer'
            elif isinstance(data, float):
                return 'number'
            elif isinstance(data, str):
                return 'string'
            elif isinstance(data, bool):
                return 'boolean'

        result = {}
        properties = {}
        required = []
        if isinstance(json_data, dict):
            result.update({'type': get_type(json_data)})
            for key, val in json_data.items():
                required.append(key)
                if isinstance(val, dict):
                    properties.update({key: Model.generate_jsonschema(val)})
                elif isinstance(val, list):
                    properties.update({key: Model.generate_jsonschema(val)})
                else:
                    properties.update(
                        {key: {'type': get_type(val), 'tittle': val.__str__(), 'description': '', 'require': True}})

            result.update({'properties': properties})
            result.update({'required': required})

        elif isinstance(json_data, list):
            result.update({'type': get_type(json_data)})
            if len(json_data) > 0:
                result.update({'items': Model.generate_jsonschema(json_data[0])})

        return result

    def import_json(self, data: dict):
        self.model = self.generate_jsonschema(data)
        self.save(self.model)




    def save(self, data: dict):
        """
        重写model的值，并保存文件
        """

        self.model = data
        FileIO.ProjIO.rewrite_model(self.proj_name, self.model_name, self.model)

    def rename(self, target_name):
        """
        修改model的名字
        """
        FileIO.ProjIO.rename_model(self.proj_name, self.model_name, target_name)
        self.model_name = target_name

class Api():
    def __init__(self, model_name: str, model: dict):
        pass


class Proj:
    def __init__(self, proj_name):
        self.proj_name = proj_name
        self.models = []
        self.apis = []

        self.fresh_models()
        self.fresh_apis()

    def fresh_models(self):
        """
        获取全部模型
        """
        models = FileIO.ProjIO.get_models(self.proj_name)
        for model in models:
            self.models.append(Model(self.proj_name, model['model_name'], model['model']))

    def fresh_apis(self):
        """
        获取全部接口信息
        """
        pass

    def export_file(self):
        pass


if __name__ == '__main__':
    proj = Proj('检查系统')
    for model in proj.models:
        print(model.model_name)
        print(model.model)
