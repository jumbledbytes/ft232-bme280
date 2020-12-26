import syslog
from enum import IntEnum


class LogLevel(IntEnum):
    DEBUG = syslog.LOG_DEBUG
    INFO = syslog.LOG_INFO
    WARNING = syslog.LOG_WARNING
    ERROR = syslog.LOG_ERR


def log(level: LogLevel, msg: str):
    syslog.syslog(level, 'ft232h-bme280: %s' % msg)
