# mvc.py - Common code for notebook
# rcampbel@purdue.edu - 2020-07-14

import nb.model
import nb.view
import nb.controller

import logging
import ipywidgets as widgets
from IPython.display import display


class AppendFileLineToLog(logging.Filter):
    """Custom logging format"""
    def filter(_, record):
        record.filename_lineno = "%s:%d" % (record.filename, record.lineno)
        return True


class NotebookLogger(logging.Handler):
    """Format log entries and make them appear in Jupyter Lab's log output"""

    def __init__(self, log_level):
        logging.Handler.__init__(self)
        self.setFormatter(logging.Formatter('%(message)s (%(filename_lineno)s)'))
        self.setLevel(log_level)
        self.log_output_widget = widgets.Output()  # NOTE This widget is not displayed

    def emit(self, message):
        """Write message to log"""
        with self.log_output_widget:
            print(self.format(message))

    def show(self):
        display(self.log_output_widget)


def run(debug=False, show_log=False):
    """Create MVC objects, start UI"""

    # Create logger
    log_level = logging.DEBUG if debug else logging.INFO
    log_handler = NotebookLogger(log_level)
    logger = logging.getLogger(__name__)
    logger.addHandler(log_handler)
    logger.addFilter(AppendFileLineToLog())
    logger.setLevel(log_level)

    # Create mvc objects
    model = nb.model.Model()
    view = nb.view.View()
    ctrl = nb.controller.Controller()

    # Give mvc objects access to each other and logger
    model.startup(view, ctrl, logger)  # Load data
    view.startup(model, ctrl, logger)  # Build user interface
    ctrl.startup(model, view, logger)  # Run the UI

    if show_log:
        log_handler.show()
