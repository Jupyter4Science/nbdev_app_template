# controller.py - Central logic for loti notebook
# rcampbel@purdue.edu - 2020-07-14

import logging
import traceback

# Avoids warning: "numpy.dtype size changed, may indicate binary incompatibility"
import warnings
warnings.filterwarnings('ignore')


class CombineLogFields(logging.Filter):
    def filter(_, record):
        record.filename_lineno = "%s:%d" % (record.filename, record.lineno)
        return True


class Controller(logging.Handler):

    VALUE = 'value'  # for observe calls

    def __init__(self, log=False, debug=False):
        self.display_log = log
        self.debugging = debug  # Add debug info to log?
        self.debug_buffer = []
        self.display_ready = False

        # Set Controller up as a logger

        if debug:
            log_format = \
                    '%(levelname)1.1s %(asctime)s %(filename_lineno)-18s %(message)s (%(funcName)s)'
            log_level = logging.DEBUG
        else:
            log_format = '%(asctime)s %(message)s'
            log_level = logging.INFO

        logging.Handler.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.setFormatter(logging.Formatter(log_format, '%Y-%m-%dT%H:%M:%S'))
        self.logger.addHandler(self)
        self.logger.addFilter(CombineLogFields())
        self.logger.setLevel(log_level)
        self.setLevel(log_level)

    def intro(self, model, view):
        '''Introduce MVC modules to each other'''
        self.model = model
        self.view = view

    def emit(self, message):
        """Pass new log msg to view for display"""
        if self.display_log:

            text = self.format(message)
            self.debug_buffer.append(text)

            if self.display_ready:

                for line in self.debug_buffer:
                    self.view.debug(line)

                self.debug_buffer = []

    def start(self):
        '''Load data, build UI, setup callbacks'''
        self.logger.debug('Starting...')

        try:
            # Load data
            self.model.get_data()

            # Set up user interface
            self.view.display(self.display_log)
            self.display_ready = True
            self.logger.debug('UI ready, log items should appear')

            # Connect UI widgets to callback methods ("cb_...").
            # These methods will be run when user changes a widget.
			# (Note: "on_click()" connects buttons, "observe()" connects other widgets.)

            # Format: self.view.<widget_to_watch>.<on_click_or_observe>(method_to_call)
            self.view.filter_btn_apply.on_click(self.cb_apply_filter)
            self.view.filter_ddn_ndisp.observe(self.cb_ndisp_changed, self.VALUE)
            self.view.filter_btn_refexp.on_click(self.cb_fill_results_export)
            self.view.plot_ddn.observe(self.cb_plot_type_selected, self.VALUE)
        except Exception as e:
            self.logger.debug('EXCEPTION\n'+traceback.format_exc())
            raise

    def cb_fill_results_export(self, _):
        """User hit button to download results"""
        self.logger.debug('At')

        try:
            # Create link for filter results
            if self.model.res_count > 0:
                filename = self.model.create_download_file(self.model.results, 'csv')
                self.view.export_link(filename, self.view.filter_out_export)
        except Exception:
            self.logger.debug('EXCEPTION\n' + traceback.format_exc())
            raise

    def cb_apply_filter(self, _):
        '''React to apply filter button press'''

        self.view.filter_out_export.clear_output()
        self.model.clear_filter_results()  # New search attempt so reset
        self.model.search(self.view.filter_txt_startyr.value, self.view.filter_txt_endyr.value)
        self.cb_refresh_filter_output()

    def cb_ndisp_changed(self, _):
        self.cb_refresh_filter_output()

    def cb_refresh_filter_output(self):
        # Enable or disable controls based on filter results
        if self.model.res_count > 0:
            self.view.update_filtered_output()
        else:
            self.view.empty_list_msg()
            # TODO Disable download

        self.view.set_plot_status()

    def cb_plot_type_selected(self, _):
        self.view.plot()
