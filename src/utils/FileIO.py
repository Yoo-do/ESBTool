import json
import os
import path_lead


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
        model_path = os.path.join(proj_path, 'models')
        if not os.path.exists(model_path):
            os.mkdir('models')
            return models

        for model in os.listdir(model_path):
            f = open(os.path.join(model_path, model), 'r', encoding='utf-8')
            data = json.load(f)
            models.append({'model_name': model.split('.')[0], 'model': data})

        return models


if __name__ == '__main__':
    # print(ProjIO.get_models('检查系统'))
    print(ProjIO.get_proj_names())