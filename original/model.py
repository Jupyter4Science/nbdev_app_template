# model.py - Storage access for app
# rcampbel@purdue.edu - 2020-07-14

import os
import csv
import glob
import pandas as pd


class Model:

    def __init__(self):
        # The models's "public" attributes are listed here, with type hints, for quick reference
        self.data: pd.DataFrame
        self.results: pd.DataFrame
        self.res_count: int = 0
        self.headers: list
        self.ymin: int
        self.ymax: int

        pd.set_option('display.width', 1000)  # Prevent data desc line breaking

    def start(self):
        """Read data and/or prepare to query data."""

        # Create module-level singletons
        global logger, Const
        from nb.cfg import logger, Const

        # Load data into memory from file
        self.data = pd.read_csv(os.path.join(Const.DATA_DIR, Const.DATA_FILE), escapechar='#')
        self.headers = list(self.data.columns.values)

        # Get values for data selection  TODO ennforce data selection limits
        self.ymin = min(self.data[self.data.columns[0]])
        self.ymax = max(self.data[self.data.columns[0]])

        logger.info('Data load completed')

    def set_disp(self, data=None, limit=None, wide=False):
        """Prep Pandas to display specific number of data lines."""
        if not limit:
            limit = data.shape[0]

        pd.set_option('display.max_rows', limit + 1)

        if wide:
            pd.set_option('display.float_format', lambda x: format(x, Const.FLOAT_FORMAT))

    def clear_filter_results(self):
        """Reset results-tracking attributes."""
        self.results = None
        self.res_count = 0

    def filter_data(self, from_year, to_year):
        '''Use provided values to filter data.'''
        self.results = self.data[(self.data[self.headers[0]] >= int(from_year)) &
                                 (self.data[self.headers[0]] <= int(to_year))]
        self.res_count = self.results.shape[0]
        logger.debug('Results: '+str(self.res_count))

    def iterate_data(self):
        """Get iterator for data."""
        return self.data.itertuples()

    def create_download_file(self, data, file_format_ext):
        """Prep data for export."""

        # First, to save space, delete existing download file(s)
        for filename in glob.glob(Const.DOWNLOAD_DATA_NAME + '.*'):
            os.remove(filename)

        # Create new download file TODO Other download formats
        filename = Const.DOWNLOAD_DATA_NAME + '.' + file_format_ext
        data.to_csv(filename, index=False, quoting=csv.QUOTE_NONNUMERIC)

        return filename
