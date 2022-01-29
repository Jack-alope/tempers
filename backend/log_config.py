"""
This file configers logging for the project.
In a file where you would like to use logging.

import logging
log = logging.getLogger(<name_of_logger>)

Setting <name_of_logger> to console logger will log to the console
Setting it to tracking_logger or main_logger will log to those files.
New loggers can also be set up to log to more specific files.

To actually call the logger

log.<log_level>(<message>)

log_level can be INFO, WARN, DEBUG
"""

from logging.config import dictConfig

LOG_LEVEL: str = "DEBUG"
FORMAT: str = (
    "%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s"
)
logging_config = {
    "version": 1,
    "formatters": {
        "basic": {
            "format": FORMAT,
        }
    },
    "handlers": {
        "console": {
            "formatter": "basic",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "level": LOG_LEVEL,
        },
        "main_handler": {
            "filename": "log/main.log",
            "class": "logging.FileHandler",
            "formatter": "basic",
        },
        "tracking_handler": {
            "filename": "log/tracking.log",
            "class": "logging.FileHandler",
            "formatter": "basic",
        },
        "sqlalchemy_handler": {
            "filename": "log/sqlalchemy.log",
            "class": "logging.FileHandler",
            "formatter": "basic",
        },
    },
    "loggers": {
        "console_logger": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
        "main_logger": {"handlers": ["main_handler"], "level": LOG_LEVEL},
        "tracking_logger": {"handlers": ["tracking_handler"], "level": LOG_LEVEL},
        "gunicorn": {"propagate": True, "handlers": ["console"]},
        "uvicorn": {"propagate": True, "handlers": ["console"]},
        "uvicorn.access": {"propagate": True, "handlers": ["console"]},
        "logger_sqlalchemy": {"handlers": ["sqlalchemy_handler"], "level": "WARN"},
        "logger_alembic": {"handlers": ["sqlalchemy_handler"], "level": "INFO"},
    },
}


def init_loggers():
    """Config logging"""

    dictConfig(logging_config)
