# cfg.py - Constants and singletons for notebook
# rcampbel@purdue.edu - 2022-01-05

import logging
import ipywidgets as widgets

from nb.model import Model
from nb.view import View
from nb.controller import Controller


class Const:
    """Store app-wide constants, including values and language text."""

    # NOTE This class is a simple catch-all. For better features, consider using the following:
    # - Multilingual internationalization: https://docs.python.org/2/library/gettext.html
    # - Data classes: https://docs.python.org/3/library/dataclasses.html
    # - Bound attributes: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s16.html

    # Data
    DATA_DIR = 'data'
    DATA_FILE = 'loti.csv'
    DOWNLOAD_DATA_NAME = 'loti-download'
    FLOAT_FORMAT = '0,.4f'

    # General
    APP_TITLE = 'Land-Ocean Temperature Index'
    CSS_JS_HTML = 'nb/custom.html'
    LOGO_IMAGE = 'nb/logo.png'
    ALL = 'All'
    EMPTY = ''
    NO_DATA_MSG = '''<br>(There's no data to display.)'''
    EXPORT_LINK_PROMPT = "Click here to save file: "
    TAB_TITLES = ['Welcome', 'Data', 'Selection', 'Visualize', 'Settings']
    PLOT_TITLE = 'Land-Ocean Temperature Index'

    # Welcome tab
    USING_TITLE = 'Using This App'
    USING_TEXT = '''<p>
    In the <b>Data</b> tab above, you can review the dataset.
    In the <b>Selection</b> tab, you can search for and download data of interest.
    Once you've selected data, generate plots in the <b>Visualize</b> tab.
    </p>'''
    SOURCES_TITLE = 'Data Sources'
    SOURCES_TEXT = '''<p>
    <b>Land-Ocean Temperature Index</b>
    <a href="https://climate.nasa.gov/vital-signs/global-temperature/"
    target="_blank">Global Temperature (NASA)</a>
    ,
    <a href="https://data.giss.nasa.gov/gistemp/"
    target="_blank">GISS Surface Temperature Analysis (NASA)</a>
    </p><p>
    This site is based on data downloaded from the following site on 2020-07-14:
    <a href="https://data.giss.nasa.gov/gistemp/graphs/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.txt"  # noqa
    target="_blank">Global Mean Estimates based on Land_and Ocean Data (NASA)</a>
    </p>'''

    # Data tab
    PREVIEW_SECTION_TITLE = 'Data'

    # Selection tab
    CRITERIA_TITLE = 'Selection Criteria'
    CRITERIA_APPLY = 'Filter'
    OUTPUT_TITLE = 'Results'
    OUTPUT_PRE = 'Limit to '
    OUTPUT_POST = 'lines'
    EXPORT_TITLE = 'Export'
    EXPORT_BUTTON = 'Create Download Link'
    START_YEAR = 'From Year'
    END_YEAR = 'To Year'

    # Visualize tab
    NOTE_TITLE = 'Note'
    NOTE_TEXT = 'The plot is based on results from the Selection tab.'
    PLOT_TITLE = 'Plot'
    PLOT_LABEL = 'Select data field'

    # Setting tab
    PLOT_SETTINGS_SECTION_TITLE = 'Plot Settings'
    THEME = 'Theme'
    THEMES = ['onedork', 'grade3', 'oceans16', 'chesterish', 'monokai', 'solarizedl', 'solarizedd']
    CONTEXT = 'Context'
    CONTEXTS = ['paper', 'notebook', 'talk', 'poster']
    FONT_SCALE = 'Font Scale'
    SPINES = 'Spines'
    GRIDLINES = 'Gridlines'
    TICKS = 'Ticks'
    GRID = 'Grid'
    FIG_WIDTH = 'Width'
    FIG_HEIGHT = 'Height'
    APPLY = 'Apply'


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


# Singletons
logger = logging.getLogger(__name__)
log_handler = NotebookLoggingHandler(logging.INFO)
logger.addHandler(log_handler)
logger.addFilter(AppendFileLineToLog())
logger.setLevel(logging.INFO)
model = Model()
view = View()
ctrl = Controller()
