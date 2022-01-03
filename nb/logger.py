# logger.py - Logging for notebook
# rcampbel@purdue.edu - 2020-07-14

import logging  # NOTE: This is Python's logging module, not this custom module
import ipywidgets as widgets
from IPython.display import display


class AppendFileLineToLog(logging.Filter):
    """Custom logging format"""
    def filter(_, record):
        record.filename_lineno = "%s:%d" % (record.filename, record.lineno)
        return True


class NotebookLoggingHandler(logging.Handler):
    """Format log entries and make them appear in Jupyter Lab's log output"""

    def __init__(self, log_level):
        logging.Handler.__init__(self)
        self.setFormatter(logging.Formatter('%(message)s (%(filename_lineno)s)'))
        self.setLevel(log_level)
        self.log_output_widget = widgets.Output()

    def emit(self, message):
        """Write message to log"""
        with self.log_output_widget:
            print(self.format(message))

    def show(self):
        display(self.log_output_widget)


logger = logging.getLogger(__name__)
log_handler = NotebookLoggingHandler(logging.INFO)
logger.addHandler(log_handler)
logger.addFilter(AppendFileLineToLog())
logger.setLevel(logging.INFO)


def set_debug(debug=False):

    if debug:
        log_handler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)


def show_log_widget(show=False):

    if show:
        log_handler.show()
