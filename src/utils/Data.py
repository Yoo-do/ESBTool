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
                        {key: {'type': get_type(val), 'title': val.__str__(), 'description': '', 'require': True}})

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

    def save(self, data: dict = None):
        """
        重写api的值，并保存文件
        """
        if data is not None:
            self.data = data
        FileIO.ApiIO.rewrite_api(self.proj_name, self.api_path, self.data)

    def get_url(self):
        return self.data.get('url')

    def set_url(self, url: str):
        self.data.update({"url": url})
        self.save()

    def get_description(self):
        return self.data.get('description')

    def set_description(self, description: str):
        self.data.update({"description": description})
        self.save()

    def get_request_name(self):
        return self.data.get('request_name')

    def set_request_name(self, request_name: str):
        self.data.update({"request_name": request_name})
        self.save()

    def get_request_path(self):
        return self.data.get('request_path')

    def set_request_path(self, request_path: str):
        self.data.update({"request_path": request_path})
        self.save()

    def get_response_name(self):
        return self.data.get('response_name')

    def set_response_name(self, response_name: str):
        self.data.update({"response_name": response_name})
        self.save()

    def get_response_path(self):
        return self.data.get('response_path')

    def set_response_path(self, response_path: str):
        self.data.update({"response_path": response_path})
        self.save()

    def get_valid(self):
        return self.data.get('valid')

    def set_valid(self, valid: bool):
        self.data.update({"valid": valid})
        self.save()

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

    def get_model_data(self, model_path: str):
        """
        获取模型数据
        """
        return FileIO.ModelIO.get_model_data(self.proj_name, model_path)

    def fresh_model_config(self):
        """
        获取模型配置
        :return:
        """
        self.model_config = FileIO.ModelIO.get_model_config(self.proj_name)

    def get_all_model_name_path(self, pre: str = '', data: dict = None):
        """
        获取每个模型的名称及路径，在接口窗口使用，模型路径用/分隔
        :return:
        """
        models = []
        if data is None:
            data = self.model_config

        for item in data:
            if item.get('is_dir') is False:
                models.append({'name': pre + item.get('name'), 'path': item.get('path')})
            else:
                models += self.get_all_model_name_path(pre + item.get('name') + '/', item.get('items'))

        return models

    def get_model_nums(self, data: dict = None):
        """
        获取模型数量
        """
        nums = 0
        if data is None:
            data = self.model_config

        for item in data:
            if item.get('is_dir') is False:
                nums += 1
            else:
                nums += self.get_model_nums(item.get('items'))

        return nums

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
        :param full_api_name: api的全路径 list
        :return:
        """
        path = ''
        api_name = full_api_name[-1]

        for index, chain_path in enumerate(full_api_name):
            if index == 0:
                items = self.api_config
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
        data = self.get_api(full_api_name).data
        source_api_name = full_api_name[-1]
        full_api_name[-1] = new_api_name
        api_path = FileIO.ApiIO.get_api_path_by_full_name(full_api_name)

        FileIO.ApiIO.add_api(self.proj_name, api_path)
        FileIO.ApiIO.rewrite_api(self.proj_name, api_path, data)

        Log.logger.info(f'复制接口 [{source_api_name}] 生成 [{new_api_name}]')

        return api_path


    def get_api_nums(self, data: dict = None):
        """
        获取模型数量
        """
        nums = 0
        if data is None:
            data = self.api_config

        for item in data:
            if item.get('is_dir') is False:
                nums += 1
            else:
                nums += self.get_api_nums(item.get('items'))

        return nums

    def export_file(self):
        pass
