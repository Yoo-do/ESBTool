import os
import json

import path_lead
import Log

"""
项目文件IO
"""

# 项目文件夹路径
PROJ_DIR = path_lead.get_path('\projs')


def generate_proj_dir():
    """
    生成projs文件夹 以防projs文件夹丢失导
    :return: None
    """
    if not os.path.exists(PROJ_DIR):
        os.mkdir(PROJ_DIR)

        Log.logger.info(f'生成了文件夹[{PROJ_DIR}]')


def get_proj_path(proj_name: str):
    """
    获取特定项目路径
    :param proj_name: str
    :return: proj_path
    """
    generate_proj_dir()
    return os.path.join(PROJ_DIR, proj_name)


def is_exists(proj_name) -> bool:
    """
    判断是否存在项目
    :param proj_name:
    :return:
    """
    return os.path.exists(get_proj_path(proj_name))


def add_proj(proj_name):
    """
    创建新项目，默认再创建models、apis文件夹及配置文件
    :param proj_name:
    :return:
    """

    if is_exists(proj_name):
        raise Exception('项目已存在')
    else:
        proj_path = get_proj_path(proj_name)
        os.mkdir(proj_path)
        # 创建对应目录
        os.mkdir(os.path.join(proj_path, 'apis'))
        os.mkdir(os.path.join(proj_path, 'models'))

        # 创建配置文件
        model_config_path = os.path.join(proj_path, 'modelConfig.json')
        api_config_path = os.path.join(proj_path, 'apiConfig.json')
        with open(model_config_path, 'w', encoding='utf-8') as f1:
            json.dump({}, f1)

        with open(api_config_path, 'w', encoding='utf-8') as f2:
            json.dump({}, f2)


def get_proj_names():
    """
    获取全部项目名称
    """
    generate_proj_dir()
    return os.listdir(PROJ_DIR)

def get_model_config(proj_name):
    """
    获取model_config
    :param proj_name:
    :return:
    """
    proj_path = get_proj_path(proj_name)
    model_config_path = os.path.join(proj_path, 'modelConfig.json')
    with open(model_config_path, 'r', encoding='utf-8') as f:
        return json.load(f)