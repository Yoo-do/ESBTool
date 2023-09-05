import logging
import path_lead

"""
日志记录
"""

formatter = logging.Formatter('[%(asctime)s] %(levelname)s: file: %(filename)s line: %(lineno)s msg: %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.DEBUG)
    # console_handler.setFormatter(formatter)
    # logger.addHandler(console_handler)

    file_handler = logging.FileHandler(path_lead.get_path('\logs\log.log'), 'w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
