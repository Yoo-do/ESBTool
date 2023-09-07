"""
IO层，负责为Data层的数据类提供IO操作
"""

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
        创建新项目，默认再创建models、apis文件夹
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

    @staticmethod
    def get_proj_names():
        """
        获取全部项目
        """
        ProjIO.generate_proj_dir()
        return os.listdir(ProjIO.PROJ_DIR)

    @staticmethod
    def get_models(proj_name) -> [{}]:
        """
        获取项目下全部model,返回models的json数据[{"model_name": xx, "model": {}}]
        """
        models = []

        proj_path = ProjIO.get_proj_path(proj_name)
        models_path = os.path.join(proj_path, 'models')
        if not os.path.exists(models_path):
            os.mkdir('models')
            return models

        for model in os.listdir(models_path):
            f = open(os.path.join(models_path, model), 'r', encoding='utf-8')
            data = json.load(f)
            models.append({'model_name': model.split('.')[0], 'model': data})

        return models

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
    def add_model(proj_name, model_path):
        """
        新增model, 此次只需要实际的路径即可, 逻辑名称配置在modelConfig中
        """
        proj_path = ProjIO.get_proj_path(proj_name)
        models_path = os.path.join(proj_path, 'models')
        if not os.path.exists(models_path):
            os.mkdir('models')

        model_file_path = os.path.join(models_path, model_path + '.json')

        if not os.path.exists(model_file_path):
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
        if not os.path.exists(model_path):
            os.mkdir('models')

        model_file_path = os.path.join(models_path, model_path + '.json')

        if os.path.exists(model_file_path):
            os.remove(model_file_path)

        with open(model_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)


if __name__ == '__main__':
    pass
    # print(ProjIO.get_models('检查系统'))
    # ProjIO.add_model('检查系统', 'test2')
    # ProjIO.delete_model('检查系统', 'test2')
    # ProjIO.rename_model('检查系统', 'test2', 'test')
