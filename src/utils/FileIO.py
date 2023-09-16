"""
IO层，负责为Data层的数据类提供IO操作
"""
import hashlib
import json
import os
import path_lead

"""
models文件夹中无额外文件夹，model文件全部直接存放
model的文件名称为model的逻辑路径取hash
model_name为model在客户端展现的名称
model_path为model的实际路径（即hash(逻辑路径))）
相关映射关系存放在modelConfig文件中
"""


class ProjIO:
    """
    项目文件IO类
    """
    PROJ_DIR = path_lead.get_path('\projs')

    @staticmethod
    def generate_proj_dir():
        if not os.path.exists(ProjIO.PROJ_DIR):
            os.mkdir(ProjIO.PROJ_DIR)

    @staticmethod
    def get_proj_path(proj_name):
        ProjIO.generate_proj_dir()
        return os.path.join(ProjIO.PROJ_DIR, proj_name)

    @staticmethod
    def is_exists(proj_name) -> bool:
        return os.path.exists(ProjIO.get_proj_path(proj_name))

    @staticmethod
    def add_proj(proj_name):
        """
        创建新项目，默认再创建models、apis文件夹, modelConfig、apiConfig文件
        :param proj_name:
        :return:
        """

        if ProjIO.is_exists(proj_name):
            raise Exception('项目已存在')
        else:
            proj_path = ProjIO.get_proj_path(proj_name)
            os.mkdir(proj_path)
            os.mkdir(os.path.join(proj_path, 'apis'))
            os.mkdir(os.path.join(proj_path, 'models'))

            with open(os.path.join(proj_path, 'modelConfig.json'), 'w', encoding='utf-8') as model_config:
                json.dump([], model_config, ensure_ascii=False)

            with open(os.path.join(proj_path, 'apiConfig.json'), 'w', encoding='utf-8') as api_config:
                json.dump([], api_config, ensure_ascii=False)

    @staticmethod
    def get_proj_names():
        """
        获取全部项目
        """
        ProjIO.generate_proj_dir()
        return os.listdir(ProjIO.PROJ_DIR)


class ModelIO:
    @staticmethod
    def get_model_data(proj_name, model_path):
        """
        根据model_path获取
        :param proj_name: 项目名称
        :param model_path: 模型实际路径名
        :return:
        """
        proj_path = ProjIO.get_proj_path(proj_name)

        models_path = os.path.join(proj_path, 'models')
        if not os.path.exists(models_path):
            os.mkdir('models')

        model_file_path = os.path.join(models_path, model_path + '.json')

        with open(model_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def get_model_config(proj_name):
        proj_path = ProjIO.get_proj_path(proj_name)
        model_config_path = os.path.join(proj_path, 'modelConfig.json')

        with open(model_config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def rewrite_model_config(proj_name, data):
        """
        回写modelConfig
        :param proj_name:
        :param data:
        :return:
        """
        proj_path = ProjIO.get_proj_path(proj_name)
        model_config_path = os.path.join(proj_path, 'modelConfig.json')

        with open(model_config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

    @staticmethod
    def add_model(proj_name, model_path):
        """
        新增model, 此次只需要实际的路径即可, 逻辑名称配置在modelConfig中
        """
        proj_path = ProjIO.get_proj_path(proj_name)
        models_path = os.path.join(proj_path, 'models')
        if not os.path.exists(models_path):
            os.mkdir('models')

        model_file_path = os.path.join(models_path, model_path + '.json')

        # 不论原来是否存在，直接重写
        data = {"type": "object", "properties": {}, "required": []}
        with open(model_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

    @staticmethod
    def delete_model(proj_name, model_path):
        """
        删除model
        """
        proj_path = ProjIO.get_proj_path(proj_name)
        models_path = os.path.join(proj_path, 'models')
        if not os.path.exists(models_path):
            os.mkdir('models')

        model_file_path = os.path.join(models_path, model_path + '.json')

        if os.path.exists(model_file_path):
            os.remove(model_file_path)

    @staticmethod
    def rename_model(proj_name, source_model_name, target_model_name):
        """
        修改项目下的model的名字
        """
        proj_path = ProjIO.get_proj_path(proj_name)
        models_path = os.path.join(proj_path, 'models')
        if not os.path.exists(models_path):
            os.mkdir('models')

        source_model_file_path = os.path.join(models_path, source_model_name + '.json')
        target_model_file_path = os.path.join(models_path, target_model_name + '.json')

        if os.path.exists(source_model_file_path):
            os.rename(source_model_file_path, target_model_file_path)

    @staticmethod
    def rewrite_model(proj_name, model_path, data: dict):
        """
        修改model的内容
        """
        proj_path = ProjIO.get_proj_path(proj_name)
        models_path = os.path.join(proj_path, 'models')
        if not os.path.exists(models_path):
            os.mkdir(models_path)

        model_file_path = os.path.join(models_path, model_path + '.json')

        if os.path.exists(model_file_path):
            os.remove(model_file_path)

        with open(model_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

    @staticmethod
    def get_model_path_by_full_name(full_model_name: []):
        """
        通过逻辑路径获取实际路径
        """
        return hashlib.md5(full_model_name.__str__().encode()).hexdigest()


class ApiIO:
    @staticmethod
    def get_api_data(proj_name, api_path):
        """
        根据api_path获取
        :param proj_name: 项目名称
        :param api_path: 接口实际路径名
        :return:
        """
        proj_path = ProjIO.get_proj_path(proj_name)

        apis_path = os.path.join(proj_path, 'apis')
        if not os.path.exists(apis_path):
            os.mkdir('apis')

        aoi_file_path = os.path.join(apis_path, api_path + '.json')

        with open(aoi_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def get_api_config(proj_name):
        proj_path = ProjIO.get_proj_path(proj_name)
        api_config_path = os.path.join(proj_path, 'apiConfig.json')

        with open(api_config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def rewrite_api_config(proj_name, data):
        """
        回写apiConfig
        :param proj_name:
        :param data:
        :return:
        """
        proj_path = ProjIO.get_proj_path(proj_name)
        api_config_path = os.path.join(proj_path, 'apiConfig.json')

        with open(api_config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

    @staticmethod
    def add_api(proj_name, api_path):
        """
        新增api, 此次只需要实际的路径即可, 逻辑名称配置在apiConfig中
        """
        proj_path = ProjIO.get_proj_path(proj_name)
        models_path = os.path.join(proj_path, 'apis')
        if not os.path.exists(models_path):
            os.mkdir('apis')

        api_file_path = os.path.join(models_path, api_path + '.json')

        # 不论原来是否存在，直接重写
        data = {"url": None, "description": None, "request_name": None, "request_path": None, "response_name": None, 'response_path': None, "valid": True}
        with open(api_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

    @staticmethod
    def delete_api(proj_name, api_path):
        """
        删除api
        """
        proj_path = ProjIO.get_proj_path(proj_name)
        apis_path = os.path.join(proj_path, 'apis')
        if not os.path.exists(apis_path):
            os.mkdir('apis')

        model_file_path = os.path.join(apis_path, api_path + '.json')

        if os.path.exists(model_file_path):
            os.remove(model_file_path)

    @staticmethod
    def rename_api(proj_name, source_api_name, target_api_name):
        """
        修改项目下的model的名字
        """
        proj_path = ProjIO.get_proj_path(proj_name)
        apis_path = os.path.join(proj_path, 'apis')
        if not os.path.exists(apis_path):
            os.mkdir('apis')

        source_api_file_path = os.path.join(apis_path, source_api_name + '.json')
        target_api_file_path = os.path.join(apis_path, target_api_name + '.json')

        if os.path.exists(source_api_file_path):
            os.rename(source_api_file_path, target_api_file_path)

    @staticmethod
    def rewrite_api(proj_name, api_path, data: dict):
        """
        修改model的内容
        """
        proj_path = ProjIO.get_proj_path(proj_name)
        apis_path = os.path.join(proj_path, 'apis')
        if not os.path.exists(apis_path):
            os.mkdir(apis_path)

        api_file_path = os.path.join(apis_path, api_path + '.json')

        if os.path.exists(api_file_path):
            os.remove(api_file_path)

        with open(api_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

    @staticmethod
    def get_api_path_by_full_name(full_api_name: []):
        """
        通过逻辑路径获取实际路径
        """
        return hashlib.md5(full_api_name.__str__().encode()).hexdigest()
