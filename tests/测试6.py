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
    log_format = '%(levelname)s: [%(asctime)s] file: %(filename)s line: %(lineno)s  %(message)s'
    logging.basicConfig(filename='log.log', filemode='w', format=log_format, level=logging.DEBUG, encoding='utf-8')

    logging.debug('this is a debug log')
    logging.info('this is a info log')
    logging.warning('this is a warning log')
    logging.error('this is a error log')
    logging.critical('this is a critical log')

    test_obj = TestClass(1)
    test_obj.set_data(5)
