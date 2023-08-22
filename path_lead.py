import os.path

"""
指引绝对路径
"""


def get_path(file_path):
    return os.path.dirname(__file__) + file_path
