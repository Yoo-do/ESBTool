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

