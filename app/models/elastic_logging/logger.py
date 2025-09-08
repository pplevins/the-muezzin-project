import logging

from .es_handler import ESHandler


class Logger:
    _logger = None

    @classmethod
    def get_logger(cls, name="data_logger",
                   index="logs", level=logging.DEBUG):
        if cls._logger:
            return cls._logger

        logger = logging.getLogger(name)
        logger.setLevel(level)
        if not logger.handlers:
            logger.addHandler(ESHandler(index))
            logger.addHandler(logging.StreamHandler())
        cls._logger = logger
        return logger
