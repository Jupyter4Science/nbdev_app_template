# view.py - User interface for notebook
# rcampbel@purdue.edu - 2020-07-14

import ipywidgets as widgets
import IPython
import logging
from IPython.display import display, clear_output


class View:
    LO10 = widgets.Layout(width='10%')
    LO15 = widgets.Layout(width='15%')
    LO20 = widgets.Layout(width='20%')

    def __init__(self):
        # Filer ("Selection" tab) controls
        self.filter_txt_startyr = None
        self.filter_txt_endyr = None
        self.filter_btn_apply = None
        self.filter_ddn_ndisp = None
        self.filter_output = None
        self.filter_btn_refexp = None
        self.filter_out_export = None

        # Plot ("Visualize" tab) controls
        self.plot_ddn = None
        self.plot_output = None

        # Settings controls
        self.theme = None
        self.context = None
        self.fscale = None
        self.spines = None
        self.gridlines = None
        self.ticks = None
        self.grid = None
        self.figsize1 = None
        self.figsize2 = None
        self.apply = None

    def start(self, log=False):
        """Make post __init__() preparations"""

        # Create module-level singletons
        global model, logger, Const
        from nb.cfg import model, logger, log_handler, Const

        # Optionally show additional info in log
        if log:
            log_handler.setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)

        # Create user interface

        tabs = widgets.Tab()

        # Set title for each tab
        for i, title in enumerate(Const.TAB_TITLES):
            tabs.set_title(i, title)

        # Build conent (widgets) for each tab
        tab_content = []
        tab_content.append(self.welcome_content())
        tab_content.append(self.data_content())
        tab_content.append(self.selection_content())
        tab_content.append(self.visualize_content())
        tab_content.append(self.settings_content())

        # Fill tabs with content
        tabs.children = tuple(tab_content)

        # Output header and tabs
        display(IPython.display.HTML(filename='nb/header.html'))  # styles, title, js
        display(tabs)
        logger.info('UI build completed')

        # Optionally show a widget containing log items
        if log:
            display(log_handler.log_output_widget)

    def section(self, title, contents):
        '''Utility method that create a collapsible widget container'''

        if type(contents) == str:
            contents = [widgets.HTML(value=contents)]

        ret = widgets.Accordion(children=tuple([widgets.VBox(contents)]))
        ret.set_title(0, title)
        return ret

    def welcome_content(self):
        '''Create widgets for introductory tab content'''
        content = []
        content.append(self.section(Const.USING_TITLE, Const.USING_TEXT))
        content.append(self.section(Const.SOURCES_TITLE, Const.SOURCES_TEXT))

        return widgets.VBox(content)

    def data_content(self):
        '''Show data tab content'''
        self.data_preview_out = widgets.Output()
        return self.section(Const.PREVIEW_SECTION_TITLE, [self.data_preview_out])

    def selection_content(self):
        '''Create widgets for selection tab content'''

        # Create widgets
        self.filter_txt_startyr = widgets.Text(description=Const.START_YEAR, value='', placeholder='')
        self.filter_txt_endyr = widgets.Text(description=Const.END_YEAR, value='', placeholder='')
        self.filter_btn_apply = widgets.Button(description=Const.CRITERIA_APPLY, icon='filter',
                                               layout=self.LO20)
        self.filter_ddn_ndisp = widgets.Dropdown(options=['25', '50', '100', Const.ALL], layout=self.LO10)
        self.filter_output = widgets.Output()
        self.filter_btn_refexp = widgets.Button(description=Const.EXPORT_BUTTON, icon='download',
                                                layout=self.LO20)
        self.filter_out_export = widgets.Output(layout={'border': '1px solid black'})

        self.set_no_data()  # Display empty list msg

        content = []

        # Section: Selection criteria

        section_list = []
        section_list.append(self.filter_txt_startyr)
        section_list.append(self.filter_txt_endyr)
        section_list.append(self.filter_btn_apply)
        content.append(self.section(Const.CRITERIA_TITLE, section_list))

        # Section: Output (with apply button)

        section_list = []

        row = []
        row.append(widgets.HTML('<div style="text-align: right;">'+Const.OUTPUT_PRE+'</div>', layout=self.LO15))
        row.append(self.filter_ddn_ndisp)
        row.append(widgets.HTML('<div style="text-align: left;">' + Const.OUTPUT_POST + '</div>', layout=self.LO10))
        section_list.append(widgets.HBox(row))

        section_list.append(widgets.HBox([self.filter_output]))  # NOTE Use "layout={'width': '90vw'}" to widen

        content.append(self.section(Const.OUTPUT_TITLE, section_list))

        # Section: Export (download)

        section_list = []
        section_list.append(widgets.VBox([self.filter_btn_refexp, self.filter_out_export]))
        content.append(self.section(Const.EXPORT_TITLE, section_list))

        return widgets.VBox(content)

    def visualize_content(self):
        '''Create widgets for visualizea tab content'''
        content = []
        content.append(self.section(Const.NOTE_TITLE, Const.NOTE_TEXT))

        self.plot_ddn = widgets.Dropdown(options=[Const.EMPTY], value=None, disabled=True)
        self.plot_output = widgets.Output()

        section_list = []

        row = []
        row.append(widgets.HTML(value=Const.PLOT_LABEL))
        row.append(widgets.Label(value='', layout=widgets.Layout(width='60%')))  # Cheat: spacer
        section_list.append(widgets.HBox(row))

        section_list.append(self.plot_ddn)
        section_list.append(self.plot_output)
        content.append(self.section(Const.PLOT_TITLE, section_list))

        return widgets.VBox(content)

    def settings_content(self):
        self.theme = widgets.Dropdown(description=Const.THEME, options=Const.THEMES)
        self.context = widgets.Dropdown(description=Const.CONTEXT, options=Const.CONTEXTS)
        self.fscale = widgets.FloatSlider(description=Const.FONT_SCALE, value=1.4)
        self.spines = widgets.Checkbox(description=Const.SPINES, value=False)
        self.gridlines = widgets.Text(description=Const.GRIDLINES, value='--')
        self.ticks = widgets.Checkbox(description=Const.TICKS, value=True)
        self.grid = widgets.Checkbox(description=Const.GRID, value=False)
        self.figsize1 = widgets.FloatSlider(description=Const.FIG_WIDTH, value=6)
        self.figsize2 = widgets.FloatSlider(description=Const.FIG_HEIGHT, value=4.5)
        self.apply = widgets.Button(description=Const.APPLY)

        return(self.section(Const.PLOT_SETTINGS_SECTION_TITLE,
                            [self.theme, self.context, self.fscale, self.spines, self.gridlines,
                             self.ticks, self.grid, self.figsize1, self.figsize2, self.apply]))

    def set_no_data(self):
        """Replace contents of filter output area with new text or data"""
        with self.filter_output:
            clear_output(wait=True)
            display(widgets.HTML(Const.NO_DATA_MSG))
