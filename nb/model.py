# model.py - Storage access for loti notebook
# rcampbel@purdue.edu - 2020-07-14

import os
import csv
import glob
import pandas as pd


class Model:

    DATA_DIR = 'data'
    DATA_FILE = 'loti.csv'
    DOWNLOAD_DATA_NAME = 'loti-download'

    def __init__(self):
        self.root = self.DATA_DIR
        self.data = None
        self.results = None
        self.res_count = 0
        self.res_csv = None
        self.headers = ''
        self.query = ''
        self.ymin = []
        self.ymax = []
        self.valid = False
        pd.set_option('display.width', 1000)  # Prevent data desc line breaking

    @staticmethod
    def start(nb_ctrl):
        """Create module-level global variable(s)"""
        global ctrl
        ctrl = nb_ctrl

    def set_disp(self, data=None, limit=None, wide=False):
        """Prep Pandas to display specific number of data lines"""
        if not limit:
            limit = data.shape[0]

        pd.set_option('display.max_rows', limit + 1)

        if wide:
            pd.set_option('display.float_format', lambda x: format(x, self.FLOAT_FORMAT))

    def get_data(self):
        '''Load data into memory from file'''
        self.data = pd.read_csv(os.path.join(self.DATA_DIR, self.DATA_FILE), escapechar='#')
        self.headers = list(self.data.columns.values)

        # Get values for data selection
        self.ymin = min(self.data[self.data.columns[0]])
        self.ymax = max(self.data[self.data.columns[0]])

        self.valid = True
        ctrl.logger.info('Data load completed')

    def clear_filter_results(self):
        self.results = None
        self.res_count = 0

    def search(self, from_year, to_year):
        '''Use provided values to filter data'''
        try:
            self.results = self.data[(self.data[self.headers[0]] >= int(from_year)) &
                                     (self.data[self.headers[0]] <= int(to_year))]
            self.res_count = self.results.shape[0]
            ctrl.logger.debug('Results: '+str(self.res_count))
        except Exception as e:
            ctrl.logger.debug('Search error!')  # TODO Add exeception text
            self.res_count = 0

    def iterate_data(self):
        return self.data.itertuples()

    def delete_downloads(self, base_name):
        """Remove any existing download file(s) of given name"""

        for filename in glob.glob(base_name + '.*'):
            os.remove(filename)

    def create_download_file(self, data, file_format_ext):
        """Prep data for export"""

        # First, to save space, delete existing download file(s)
        self.delete_downloads(self.DOWNLOAD_DATA_NAME)

        # Create new download file TODO Other download formats
        filename = self.DOWNLOAD_DATA_NAME + '.' + file_format_ext
        data.to_csv(filename, index=False, quoting=csv.QUOTE_NONNUMERIC)

        return filename
