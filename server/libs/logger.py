import logging
from logging.handlers import TimedRotatingFileHandler

system_logging_name = 'root'


def log():
    return logging.getLogger(system_logging_name)


def configure_logging():
    # System wide logging
    logger = logging.getLogger(system_logging_name)

    log_fh = TimedRotatingFileHandler('logs/log', when='midnight', backupCount=30)
    log_fh.suffix = '%Y_%m_%d'
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)')
    log_fh.setFormatter(formatter)

    stderr_fh = logging.StreamHandler()

    logger.addHandler(log_fh)
    logger.addHandler(stderr_fh)
    logger.setLevel(logging.DEBUG)

    return logger
