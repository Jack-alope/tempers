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
    },
    "loggers": {
        "console_logger": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            # "propagate": False
        },
        "main_logger": {"handlers": ["main_handler"], "level": LOG_LEVEL},
        "tracking_logger": {"handlers": ["tracking_handler"], "level": LOG_LEVEL},
    },
}


def init_loggers():
    dictConfig(logging_config)
