"""
数据模型层，为前端窗体提供数据结构支持
"""
import json
import jsonschema
from src.utils import FileIO, Log

ModelDataTypes = ['object', 'array', 'integer', 'number', 'string', 'boolean']


class Model:
    """
    数据模型类
    """

    def __init__(self, proj_name: str, model_name: str, model_path: str, model: dict):
        self.proj_name = proj_name
        self.model_name = model_name
        self.model_path = model_path
        self.model = model

    def validate(self, data: dict) -> bool:
        try:
            jsonschema.validate(data, self.model)
            return True
        except jsonschema.ValidationError as e:
            raise Exception((e.path).__str__() + ' : ' + e.message.__str__())

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
        FileIO.ProjIO.rewrite_model(self.proj_name, self.model_path, self.model)

    def delete(self):
        """
        删除model文件
        :return:
        """
        FileIO.ProjIO.delete_model(self.proj_name, self.model_path)


class Api:
    """
    接口对应数据类
    """

    def __init__(self, api_name: str):
        pass


class Proj:
    def __init__(self, proj_name):
        self.proj_name = proj_name
        self.model_config = {}
        self.apis = []

        self.fresh_apis()
        self.fresh_model_config()

    def get_model(self, full_model_name: list):
        """
        根据名称获取对应的model对象
        :param full_model_name: model的全路径 list
        :return:
        """
        path = ''
        model_name = full_model_name[-1]

        for index, chain_path in enumerate(full_model_name):
            if index == 0:
                items = self.model_config
            else:
                items = path.get('items')

            path = [x for x in items if x.get('name') == chain_path][0]

        model_path = path.get('path')
        model = Model(self.proj_name, model_name, model_path, FileIO.ProjIO.get_model_data(self.proj_name, model_path))
        return model

    def fresh_model_config(self):
        """
        获取模型配置
        :return:
        """
        self.model_config = FileIO.ProjIO.get_model_config(self.proj_name)

    def delete_model(self, full_model_name):
        """
        删除项目中的模型
        :param full_model_name:
        :return:
        """
        target_model = self.get_model(full_model_name)
        target_model.delete()
        Log.logger.info(f'项目 [{self.proj_name}] 删除了模型 [{full_model_name[-1]}]')
        self.fresh_model_config()


    def add_model(self, full_model_name):
        """
        项目中新增模型
        :param full_model_name: 当前模型的全逻辑路径
        :return:
        """
        model_path = FileIO.ProjIO.get_model_path_by_full_name(full_model_name)
        FileIO.ProjIO.add_model(self.proj_name, model_path)
        Log.logger.info(f'项目 [{self.proj_name}] 新增了模型 [{full_model_name[-1]}] ')
        self.fresh_model_config()



    def fresh_apis(self):
        """
        获取全部接口信息
        """
        pass

    def export_file(self):
        pass


if __name__ == '__main__':
    pass
    # proj = Proj('检查系统')
    # for model in proj.models:
    #     print(model.model_name)
    #     print(model.model)
