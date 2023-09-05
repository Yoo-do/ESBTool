"""
IO层，负责为Data层的数据类提供IO操作
"""

import json
import os
import path_lead
import Log


class ProjIO:
    """
    项目文件IO类
    """

    # 项目文件夹
    PROJ_DIR = path_lead.get_path('\projs')

    @staticmethod
    def generate_proj_dir():
        """
        生成projs文件夹
        :return:
        """
        if not os.path.exists(ProjIO.PROJ_DIR):
            os.mkdir(ProjIO.PROJ_DIR)

            Log.logger.info(f'生成了文件夹[{ProjIO.PROJ_DIR}]')

    @staticmethod
    def get_proj_path(proj_name):
        """
        获取对于项目路径
        :param proj_name:
        :return:
        """
        ProjIO.generate_proj_dir()
        return os.path.join(ProjIO.PROJ_DIR, proj_name)

    @staticmethod
    def is_exists(proj_name) -> bool:
        """
        判断是否存在项目
        :param proj_name:
        :return:
        """
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
        model_path = os.path.join(proj_path, 'models')
        if not os.path.exists(model_path):
            os.mkdir('models')
            return models

        for model in os.listdir(model_path):
            f = open(os.path.join(model_path, model), 'r', encoding='utf-8')
            data = json.load(f)
            models.append({'model_name': model.split('.')[0], 'model': data})

        return models

    @staticmethod
    def add_model(proj_name, model_name):
        """
        新增model
        """
        proj_path = ProjIO.get_proj_path(proj_name)
        model_path = os.path.join(proj_path, 'models')
        if not os.path.exists(model_path):
            os.mkdir('models')

        model_file_path = os.path.join(model_path, model_name + '.json')

        if not os.path.exists(model_file_path):
            data = {"type": "object", "properties": {}, "required": []}
            with open(model_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)

    @staticmethod
    def delete_model(proj_name, model_name):
        """
        删除model
        """
        proj_path = ProjIO.get_proj_path(proj_name)
        model_path = os.path.join(proj_path, 'models')
        if not os.path.exists(model_path):
            os.mkdir('models')

        model_file_path = os.path.join(model_path, model_name + '.json')

        if os.path.exists(model_file_path):
            os.remove(model_file_path)

    @staticmethod
    def rename_model(proj_name, source_model_name, target_model_name):
        """
        修改项目下的model的名字
        """
        proj_path = ProjIO.get_proj_path(proj_name)
        model_path = os.path.join(proj_path, 'models')
        if not os.path.exists(model_path):
            os.mkdir('models')

        source_model_file_path = os.path.join(model_path, source_model_name + '.json')
        target_model_file_path = os.path.join(model_path, target_model_name + '.json')

        if os.path.exists(source_model_file_path):
            os.rename(source_model_file_path, target_model_file_path)

    @staticmethod
    def rewrite_model(proj_name, model_name, data: dict):
        """
        修改model的内容
        """
        proj_path = ProjIO.get_proj_path(proj_name)
        model_path = os.path.join(proj_path, 'models')
        if not os.path.exists(model_path):
            os.mkdir('models')

        model_file_path = os.path.join(model_path, model_name + '.json')

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
    ProjIO.rewrite_model('检查系统', 'test', {"type": "object", "properties": {
        "id": {"type": "string", "tittle": "消息id", "description": "", "require": True}}, "required": []})
