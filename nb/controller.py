# controller.py - Central logic for loti notebook
# rcampbel@purdue.edu - 2020-07-14
import nb.mvc

import logging
import traceback
from jupyterthemes import jtplot


class AppendFileLineToLog(logging.Filter):
    """Custom logging format"""
    def filter(_, record):
        record.filename_lineno = "%s:%d" % (record.filename, record.lineno)
        return True


class Controller(logging.Handler):

    def __init__(self, log_level=logging.DEBUG):  # to reduce log activity, send logging.INFO
        # Set Controller up as a logger
        logging.Handler.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.setFormatter(logging.Formatter('%(message)s (%(filename_lineno)s)'))
        self.logger.addHandler(self)
        self.logger.addFilter(AppendFileLineToLog())
        self.logger.setLevel(log_level)
        self.setLevel(log_level)

    @staticmethod
    def start():
        global model
        global view
        model = nb.mvc.model
        view = nb.mvc.view

    def emit(self, message):
        """Write message to log"""
        with view.log_output_widget:
            print(self.format(message))

    def run(self):
        '''Load data, build UI, setup callbacks'''
        self.logger.info('Starting...')

        try:
            # Load data
            model.get_data()

            # Set up user interface
            view.display()
            self.display_ready = True
            self.logger.debug('UI should be ready')

            # Connect UI widgets to callback methods ("cb_...").
            # These methods will be run when user changes a widget.
            # NOTE "on_click()" connects buttons, "observe()" connects other widgets.
            view.filter_btn_apply.on_click(self.cb_apply_filter)
            view.filter_ddn_ndisp.observe(self.cb_ndisp_changed, 'value')
            view.filter_btn_refexp.on_click(self.cb_fill_results_export)
            view.plot_ddn.observe(self.cb_plot_type_selected, 'value')
            view.apply.on_click(self.cb_apply_theme)
        except Exception:
            self.logger.debug('EXCEPTION\n'+traceback.format_exc())
            raise

    def cb_fill_results_export(self, _):
        """User hit button to download results"""

        try:
            # Create link for filter results
            if model.res_count > 0:
                filename = model.create_download_file(model.results, 'csv')
                view.export_link(filename, view.filter_out_export)
        except Exception:
            self.logger.debug('EXCEPTION\n' + traceback.format_exc())
            raise

    def cb_apply_filter(self, _):
        '''React to apply filter button press'''

        view.filter_out_export.clear_output()
        model.clear_filter_results()  # New search attempt so reset
        model.search(view.filter_txt_startyr.value, view.filter_txt_endyr.value)
        self.cb_refresh_filter_output()

    def cb_ndisp_changed(self, _):
        self.cb_refresh_filter_output()

    def cb_refresh_filter_output(self):
        # Enable or disable controls based on filter results
        if model.res_count > 0:
            view.update_filtered_output()
        else:
            view.empty_list_msg()
            # TODO Disable download

        view.set_plot_status()

    def cb_plot_type_selected(self, _):
        view.plot()

    def cb_apply_theme(self, _):
        jtplot.style(theme=view.theme.value,
                     context=view.context.value,
                     fscale=view.fscale.value,
                     spines=view.spines.value,
                     gridlines=view.gridlines.value,
                     ticks=view.ticks.value,
                     grid=view.grid.value,
                     figsize=(view.figsize1.value, view.figsize2.value))
        jtplot.reset()
