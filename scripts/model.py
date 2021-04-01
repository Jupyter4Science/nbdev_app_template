# model.py - Storage access for scsa notebook
# rcampbel@purdue.edu - 2020-07-14

import os
import sys
import time
import pandas as pd

class Model:

    DATA_DIR  = 'data'
    DATA_FILE = 'loti.csv'
    YEAR      = '#Year'

    def __init__(self):
        self.view      = None
        self.ctrl      = None
        self.root      = self.DATA_DIR
        self.data      = None
        self.results   = None
        self.res_count = 0
        self.res_csv   = None
        self.headers   = ''
        self.query     = ''
        self.ymin      = []
        self.ymax      = []
        self.valid     = False

        pd.set_option('display.width', 1000) # Prevent data description from line breaking

    def intro(self,view,ctrl):
        '''Introduce MVC modules to each other'''
        self.view = view
        self.ctrl = ctrl

    def set_disp(self, data=None, limit=None, wide=False):
        """Prep Pandas to display specific number of data lines"""

        if not limit:
            limit = data.shape[0]

        pd.set_option('display.max_rows', limit + 1)

        if wide:
            pd.set_option('display.float_format', lambda x: format(x, self.FLOAT_FORMAT))

    def get_data(self):
        '''Load data into memory from file'''

        self.data    = pd.read_csv(os.path.join(self.DATA_DIR,self.DATA_FILE))
        self.headers = self.data.head()

        # Get values for data selection
        self.ymin  = min(self.data[self.data.columns[0]])
        self.ymax  = max(self.data[self.data.columns[0]])

        self.valid = True

        self.ctrl.logger.debug('Data load completed')

    def clear_filter_results(self):
        self.results   = None
        self.res_count = 0

    def search(self,from_year,to_year):
        '''Use provided values lists to search for data'''
        self.ctrl.logger.debug('-')

        # Build query string
        self.query = self.YEAR+' >= '+str(from_year) #+' and '+self.YEAR+' <= '+str(to_year)
        self.ctrl.logger.debug('Query string: "'+self.query+'"')

        # Run query
        self.results   = self.data[(self.data['#Year'] >= int(from_year)) & (self.data['#Year'] <= int(to_year))]
        self.res_count = self.results.shape[0]
        self.ctrl.logger.debug('Results: '+str(self.res_count))

    def sort(self,col_list):
        self.results = self.results.sort_values(by=[self.YEAR])

    def iterate_data(self):
        return self.data.itertuples()

    def iterate_results(self):
        return self.results.itertuples()

    def write_results(self):
        '''Prep data for export'''
        self.res_csv = ','.join(self.headers) + '\n'

        for i,row in enumerate(self.iterate_results()):
            self.res_csv += ','.join([str(row)]) + '\n' # TODO fix this

        self.ctrl.logger.debug('Rendered CSV')



