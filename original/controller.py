# controller.py - Central logic for app
# rcampbel@purdue.edu - 2020-07-14

import traceback
from IPython.display import display, clear_output, FileLink
from jupyterthemes import jtplot
from matplotlib import pyplot as plt


class Controller():

    def start(self):
        """Begin running the app."""

        # Create module-level singletons
        global model, view, logger, Const
        from nb.cfg import model, view, logger, Const

        # Show data preview
        with view.data_preview_out:
            display(model.data)

        # Setup callbacks
        try:
            # Connect UI widgets to callback methods ("cb_...").
            # These methods will be run when user changes a widget.
            # NOTE "on_click()" connects buttons, "observe()" connects other widgets.
            view.filter_btn_apply.on_click(self.cb_apply_filter)
            view.filter_ddn_ndisp.observe(self.cb_ndisp_changed, 'value')
            view.filter_btn_refexp.on_click(self.cb_fill_results_export)
            view.plot_ddn.observe(self.cb_plot_type_selected, 'value')
            view.apply.on_click(self.cb_apply_plot_settings)
            logger.info('App running')
        except Exception:
            logger.debug('Exception while setting up callbacks...\n'+traceback.format_exc())
            raise

    def cb_fill_results_export(self, _):
        """React to user pressing button to download results."""
        try:
            # Create link for filter results
            if model.res_count > 0:
                filename = model.create_download_file(model.results, 'csv')

                with view.filter_out_export:
                    clear_output(wait=True)
                    display(FileLink(filename, result_html_prefix=Const.EXPORT_LINK_PROMPT))

        except Exception:
            logger.debug('Exception during download creation...\n' + traceback.format_exc())
            raise

    def cb_apply_filter(self, _):
        """React to apply filter button press."""
        try:
            view.filter_out_export.clear_output()
            model.clear_filter_results()  # New search attempt so reset
            model.filter_data(view.filter_txt_startyr.value, view.filter_txt_endyr.value)
            self.refresh_filter_output()
        except Exception:
            logger.debug('Exception while filtering data...\n'+traceback.format_exc())

    def cb_ndisp_changed(self, _):
        """React to user changing result page size."""
        try:
            self.refresh_filter_output()
        except Exception:
            logger.debug('Exception while changing number of out lines to display...\n'+traceback.format_exc())

    def cb_plot_type_selected(self, _):
        """React to use requesting plot."""
        try:

            if not view.plot_ddn.value == Const.EMPTY:
                view.plot_output.clear_output(wait=True)
                # TODO Add ability to download plot as an image

                with view.plot_output:
                    plt.plot(model.results[model.headers[0]], model.results[view.plot_ddn.value])
                    plt.xlabel(model.headers[0])
                    plt.ylabel(view.plot_ddn.value)
                    plt.suptitle(Const.PLOT_TITLE)
                    plt.show()
                    logger.debug('Plot finished')
        except Exception:
            logger.debug('Exception while plotting...')
            raise
        finally:
            plt.close()

    def cb_apply_plot_settings(self, _):
        """React to user applying settings"""
        try:
            jtplot.style(theme=view.theme.value,
                         context=view.context.value,
                         fscale=view.fscale.value,
                         spines=view.spines.value,
                         gridlines=view.gridlines.value,
                         ticks=view.ticks.value,
                         grid=view.grid.value,
                         figsize=(view.figsize1.value, view.figsize2.value))
        except Exception:
            logger.debug('Exception while applying plot settings...')
            raise

    def refresh_filter_output(self):
        """Display filter results. Enable/disable plot widget(s)."""

        if model.res_count > 0:

            # Calc set output line limit
            if view.filter_ddn_ndisp.value == Const.ALL:
                limit = model.res_count
            else:
                limit = int(view.filter_ddn_ndisp.value)

            # Display results

            model.set_disp(limit=limit)

            with view.filter_output:
                clear_output(wait=True)
                display(model.results.head(limit))

            # Enable plot
            view.plot_ddn.disabled = False
            view.plot_ddn.options = [Const.EMPTY]+model.headers[1:]
        else:
            view.set_no_data()  # Show "empty list" msg
            view.plot_ddn.disabled = True
