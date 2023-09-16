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
        FileIO.ModelIO.rewrite_model(self.proj_name, self.model_path, self.model)

    def delete(self):
        """
        删除model文件
        :return:
        """
        FileIO.ModelIO.delete_model(self.proj_name, self.model_path)


class Api:
    """
    接口对应数据类
    """

    def __init__(self, proj_name: str, api_name: str, api_path: str, data: dict):
        self.proj_name = proj_name
        self.api_name = api_name
        self.api_path = api_path
        self.data = data

    def load_data(self):
        """
        解析data
        请求的url
        详细说明
        请求的模型名称及地址
        响应的模型名称及地址
        是否在用
        """
        pass

    def save(self, data: dict):
        """
        重写api的值，并保存文件
        """

        self.data = data
        FileIO.ApiIO.rewrite_api(self.proj_name, self.api_path, self.data)

    def delete(self):
        """
        删除api文件
        :return:
        """
        FileIO.ApiIO.delete_api(self.proj_name, self.api_path)


class Proj:
    def __init__(self, proj_name):
        self.proj_name = proj_name

        self.model_config = {}
        self.api_config = {}

        self.fresh_model_config()
        self.fresh_api_config()

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
        model = Model(self.proj_name, model_name, model_path, FileIO.ModelIO.get_model_data(self.proj_name, model_path))
        return model

    def fresh_model_config(self):
        """
        获取模型配置
        :return:
        """
        self.model_config = FileIO.ModelIO.get_model_config(self.proj_name)

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
        model_path = FileIO.ModelIO.get_model_path_by_full_name(full_model_name)
        FileIO.ModelIO.add_model(self.proj_name, model_path)
        Log.logger.info(f'项目 [{self.proj_name}] 新增了模型 [{full_model_name[-1]}] ')
        self.fresh_model_config()

    def duplicate_model(self, full_mode_name, new_model_name):
        """
        复制新的模型， 并返回实际路径
        """
        data = self.get_model(full_mode_name).model
        source_model_name = full_mode_name[-1]
        full_mode_name[-1] = new_model_name
        model_path = FileIO.ModelIO.get_model_path_by_full_name(full_mode_name)

        FileIO.ModelIO.add_model(self.proj_name, model_path)
        FileIO.ModelIO.rewrite_model(self.proj_name, model_path, data)

        Log.logger.info(f'复制模型 [{source_model_name}] 生成 [{new_model_name}]')

        return model_path

    def get_api(self, full_api_name: list):
        """
        根据名称获取对应的api对象
        :param full_api_name: model的全路径 list
        :return:
        """
        path = ''
        api_name = full_api_name[-1]

        for index, chain_path in enumerate(full_api_name):
            if index == 0:
                items = self.model_config
            else:
                items = path.get('items')

            path = [x for x in items if x.get('name') == chain_path][0]

        api_path = path.get('path')
        api = Api(self.proj_name, api_name, api_path, FileIO.ApiIO.get_api_data(self.proj_name, api_path))
        return api

    def fresh_api_config(self):
        """
        获取接口配置信息
        """
        self.api_config = FileIO.ApiIO.get_api_config(self.proj_name)

    def delete_api(self, full_api_name):
        """
        删除项目中的接口
        :param full_api_name:
        :return:
        """
        target_api = self.get_api(full_api_name)
        target_api.delete()
        Log.logger.info(f'项目 [{self.proj_name}] 删除了接口 [{full_api_name[-1]}]')
        self.fresh_api_config()


    def add_api(self, full_api_name):
        """
        项目中新增模型
        :param full_api_name: 当前接口的全逻辑路径
        :return:
        """
        api_path = FileIO.ApiIO.get_api_path_by_full_name(full_api_name)
        FileIO.ApiIO.add_api(self.proj_name, api_path)
        Log.logger.info(f'项目 [{self.proj_name}] 新增了接口 [{full_api_name[-1]}] ')
        self.fresh_model_config()

    def duplicate_api(self, full_api_name, new_api_name):
        """
        复制新的模型， 并返回实际路径
        """
        data = self.get_model(full_api_name).model
        source_api_name = full_api_name[-1]
        full_api_name[-1] = new_api_name
        api_path = FileIO.ApiIO.get_api_path_by_full_name(full_api_name)

        FileIO.ApiIO.add_api(self.proj_name, api_path)
        FileIO.ApiIO.rewrite_api(self.proj_name, api_path, data)

        Log.logger.info(f'复制接口 [{source_api_name}] 生成 [{new_api_name}]')

        return api_path

    def export_file(self):
        pass


if __name__ == '__main__':
    pass
    # proj = Proj('检查系统')
    # for model in proj.models:
    #     print(model.model_name)
    #     print(model.model)
