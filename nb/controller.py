# controller.py - Central logic for loti notebook
# rcampbel@purdue.edu - 2020-07-14

import logging
import traceback

from nb import model, view


class Controller(logging.Handler):

    def __init__(self, model, view, log_level=logging.DEBUG):  # to reduce log activity, send logging.INFO

        # Ensure mvc objs have refs to each other
        self.model = model
        self.view = view
        self.view.model = model
        self.view.ctrl = self
        self.model.view = view
        self.model.ctrl = self

        # Set Controller up as a logger
        logging.Handler.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.setFormatter(logging.Formatter('%(message)s (%(filename_lineno)s)'))
        self.logger.addHandler(self)
        self.logger.addFilter(AppendFileLineToLog())
        self.logger.setLevel(log_level)
        self.setLevel(log_level)

    def emit(self, message):
        """Write message to log"""
        with view.log_output_widget:
            print(self.format(message))

    def start(self):
        '''Load data, build UI, setup callbacks'''
        self.logger.info('Starting...')

        try:
            # Load data
            self.model.get_data()

            # Set up user interface
            self.view.display()
            self.display_ready = True
            self.logger.debug('UI should be ready')

            # Connect UI widgets to callback methods ("cb_...").
            # These methods will be run when user changes a widget.
            # (Note: "on_click()" connects buttons, "observe()" connects other widgets.)

            # Format: self.view.<widget_to_watch>.<on_click_or_observe>(method_to_call)
            self.view.filter_btn_apply.on_click(self.cb_apply_filter)
            self.view.filter_ddn_ndisp.observe(self.cb_ndisp_changed, 'value')
            self.view.filter_btn_refexp.on_click(self.cb_fill_results_export)
            self.view.plot_ddn.observe(self.cb_plot_type_selected, 'value')
        except Exception as e:
            self.logger.debug('EXCEPTION\n'+traceback.format_exc())
            raise

    def cb_fill_results_export(self, _):
        """User hit button to download results"""

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


class AppendFileLineToLog(logging.Filter):
    def filter(_, record):
        record.filename_lineno = "%s:%d" % (record.filename, record.lineno)
        return True


def run():
    '''Create user interface, set up callbacks, start event loop'''
    # Create MVC objs, into to one another
    nb_model = model.Model()
    nb_view = view.View()
    nb_ctrl = Controller(nb_model, nb_view)
    nb_ctrl.start()  # Run the notebook
