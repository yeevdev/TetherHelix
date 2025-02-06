import logging
import os
from datetime import datetime


class Logger:
    _instance = None

    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter("[%(asctime)s][%(levelname)-7s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

        log_dir = "./logs"
        os.makedirs(log_dir, exist_ok=True)

        log_filename = log_dir + f"/{current_time}.log"
        file_handler = logging.FileHandler(log_filename, encoding="UTF-8")
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)


    @classmethod
    def get_logger(cls) -> logging.Logger:
        if not cls._instance:
            cls._instance = Logger()
        return cls._instance.logger