# mvc.py - Common code for loti notebook
# rcampbel@purdue.edu - 2020-07-14

import nb.model
import nb.view
import nb.controller

import logging
import ipywidgets as widgets


class AppendFileLineToLog(logging.Filter):
    """Custom logging format"""
    def filter(_, record):
        record.filename_lineno = "%s:%d" % (record.filename, record.lineno)
        return True


class NotebookLogger(logging.Handler):

    def __init__(self, log_level):
        logging.Handler.__init__(self)
        self.setFormatter(logging.Formatter('%(message)s (%(filename_lineno)s)'))
        self.setLevel(log_level)
        self.log_output_widget = widgets.Output()  # NOTE This widget is not displayed

    def emit(self, message):
        """Write message to log"""
        with self.log_output_widget:
            print(self.format(message))


def run(log_level=logging.DEBUG):  # NOTE Use logging.INFO to reduce log activity
    """Create MVC objects, start UI"""

    # Create logger
    logger = logging.getLogger(__name__)
    logger.addHandler(NotebookLogger(log_level))
    logger.addFilter(AppendFileLineToLog())
    logger.setLevel(log_level)

    # Create mvc objects
    model = nb.model.Model()
    view = nb.view.View()
    ctrl = nb.controller.Controller()

    # Give mvc objects access to each other and logger
    model.start(view, ctrl, logger)
    view.start(model, ctrl, logger)
    ctrl.start(model, view, logger)

    # Run the UI
    ctrl.run()
