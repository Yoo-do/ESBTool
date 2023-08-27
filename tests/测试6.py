import logging


class TestClass:
    def __init__(self, data: int):
        logging.debug(f"data 初始化的值为: {data}")
        self.data = data


    def set_data(self, data):
        logging.debug(f"data: {self.data} -> {data}")
        self.data = data

    def get_data(self):
        logging.debug(f"获取了 data 的值: {self.data}")
        return self.data


if __name__ == '__main__':
    test = TestClass(1)