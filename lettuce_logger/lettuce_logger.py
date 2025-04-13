import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import tempfile
from typing import Union, TypeVar, Generic
import inspect

# --------------------------
# Config
# --------------------------
LOG_SIZE = 500000
LOG_BACKUP = 3
PP_LEVEL = 15
logging.addLevelName(PP_LEVEL, "PP")
T = TypeVar("T")


# --------------------------
# Path Resolver
# --------------------------
def resolve_log_path(project: Union[str, Path, None]) -> Path:
    if project is None:
        path = Path(tempfile.gettempdir()) / "lettuce_logger"
    elif isinstance(project, Path):
        path = project.expanduser().resolve()
    elif isinstance(project, str):
        path = (Path(tempfile.gettempdir()) / "lettuce_logger" / project).resolve()
    else:
        raise TypeError("project must be a str, Path, or None")

    path.mkdir(parents=True, exist_ok=True)
    return path


# --------------------------
# Logger Class
# --------------------------
class LettuceLogger(logging.Logger):
    def __init__(self, name: str, project: Union[str, Path, None] = None):
        super().__init__(name)
        log_dir = resolve_log_path(project)
        self.log_dir = log_dir
        self.setLevel(logging.DEBUG)
        self._configure_handlers(log_dir)

    def _configure_handlers(self, log_dir: Path):
        formatter = logging.Formatter(
            "%(asctime)s|%(filename)s:%(lineno)d|%(levelname)s: %(message)s",
            "%m-%d %H:%M:%S",
        )
        console_formatter = IpythonCellFormatter("%(funcName)s@%(filename)s:%(lineno)d| %(message)s", "%m-%d %H:%M:%S")

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.NOTSET)
        stream_handler.setFormatter(console_formatter)
        self.stream_handler = stream_handler
        self.addHandler(stream_handler)

        self._add_file_handler(log_dir / f"{self.name}.log", formatter, logging.DEBUG)
        self._add_file_handler(log_dir / "all_info.log", formatter, logging.INFO)
        self._add_file_handler(log_dir / "all_warning.log", formatter, logging.WARNING)
        self._add_file_handler(log_dir / "all_pp.log", formatter, PP_LEVEL)

    def _add_file_handler(self, path: Path, formatter, level: int):
        fh = RotatingFileHandler(path, maxBytes=LOG_SIZE, backupCount=LOG_BACKUP)
        fh.setFormatter(formatter)
        fh.setLevel(level)
        self.addHandler(fh)

    def pp(self, message: str, *args, **kwargs):
        self._log(PP_LEVEL, message, args, **kwargs)

    def show_pp(self):
        self.setLevel(PP_LEVEL)
        self.stream_handler.setLevel(PP_LEVEL)

    def hide_pp(self):
        self.setLevel(logging.INFO)
        self.stream_handler.setLevel(logging.INFO)


import traceback


class IpythonCellFormatter(logging.Formatter):
    def format(self, record):
        if "ipython-input" in record.filename:
            record.filename = "ipy"
        return super().format(record)


# --------------------------
# Global logger (default)
# --------------------------
_default_logger = None


# --------------------------
# Factory Function
# --------------------------
def get_logger(name="lettuce_logger", project=None) -> LettuceLogger:
    global _default_logger
    logger = LettuceLogger(name, project)
    _default_logger = logger
    return logger


# --------------------------
# Utility functions
# --------------------------


def show_pp():
    _default_logger.show_pp()  # type: ignore


def hide_pp():
    _default_logger.hide_pp()  # type: ignore


def get_log_dir():
    return _default_logger.log_dir  # type: ignore


# --------------------------
# Default Logger Accessor
# --------------------------
def set_default_logger(new_logger: LettuceLogger):
    global _default_logger
    _default_logger = new_logger


# --------------------------
# Global instance (initial default)
# --------------------------
_default_logger = get_logger()


# --------------------------
# pp function
# --------------------------
def pp(x: T) -> T:  # type: ignore
    """Log the variable with its name and return it untouched."""
    log = _default_logger
    try:
        frame = inspect.currentframe().f_back  # type: ignore
        call_line = inspect.getframeinfo(frame).code_context[0]  # type: ignore
        start = call_line.find("pp(") + 3
        end = call_line.find(")", start)
        var_name = call_line[start:end].strip()
    except Exception:
        var_name = "var"

    if isinstance(x, str):
        log.pp(x, stacklevel=3)  # type: ignore
    else:
        stringified = repr(x)
        if "\n" in stringified:
            log.pp(f"{var_name} =\n{stringified}", stacklevel=3)  # type: ignore
        else:
            log.pp(f"{var_name} = {stringified}", stacklevel=3)  # type: ignore

    return x
