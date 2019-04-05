import codecs
from threading import Lock
from src.server import config


class UiFileWriter:
    def __init__(self):
        self.lock = Lock()

    def write(self, data):
        self.lock.acquire()
        file_object = codecs.open(config.UI_DATA_FILENAME, config.FILE_APPEND_MODE, encoding=config.FILE_ENCODING)
        file_object.write(data + config.FILE_DELIMITER)
        file_object.close()
        self.lock.release()
