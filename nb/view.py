# view.py - User interface for notebook
# rcampbel@purdue.edu - 2020-07-14

import ipywidgets as widgets
import urllib
import IPython
from matplotlib import pyplot as plt
from IPython.display import display, FileLink


class View:
    EMPTY_LIST_MSG = '''<br>(There's no data to display.)'''
    ALL = 'All'
    EMPTY = ''
    FILTER_PROG = 'Searching...'
    EXPORT_LINK_PROMPT = "Click here to save file: "
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

    def section(self, title, contents):
        '''Utility method that create a collapsible widget container'''

        if type(contents) == str:
            contents = [widgets.HTML(value=contents)]

        ret = widgets.Accordion(children=tuple([widgets.VBox(contents)]))
        ret.set_title(0, title)
        return ret

    def startup(self, mvc_model, mvc_ctrl, mvc_logger):
        """Make post __init__() preparations"""

        # Create module-level global variable(s)
        global ctrl
        global model
        global logger
        ctrl = mvc_ctrl
        model = mvc_model
        logger = mvc_logger

        # Create user interface

        TITLES = ['Welcome', 'Data', 'Selection', 'Visualize', 'Settings']

        tabs = widgets.Tab()

        # Set title for each tab
        for i in range(len(TITLES)):
            tabs.set_title(i, TITLES[i])

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

    def welcome_content(self):
        '''Create widgets for introductory tab content'''
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

        content = []
        content.append(self.section(USING_TITLE, USING_TEXT))
        content.append(self.section(SOURCES_TITLE, SOURCES_TEXT))

        return widgets.VBox(content)

    def data_content(self):
        '''Show data tab content'''
        SECTION_TITLE = 'Data'

        out = widgets.Output()

        with out:
            display(model.data)

        return self.section(SECTION_TITLE, [out])

    def selection_content(self):
        '''Create widgets for selection tab content'''
        CRITERIA_TITLE = 'Selection Criteria'
        CRITERIA_APPLY = 'Search'
        OUTPUT_TITLE = 'Results'
        OUTPUT_PRE = 'Limit to '
        OUTPUT_POST = 'lines'
        EXPORT_TITLE = 'Export'
        EXPORT_BUTTON = 'Create Download Link'
        START_YEAR = 'From Year'
        END_YEAR = 'To Year'

        # Create widgets
        self.filter_txt_startyr = widgets.Text(description=START_YEAR, value='', placeholder='')
        self.filter_txt_endyr = widgets.Text(description=END_YEAR, value='', placeholder='')
        self.filter_btn_apply = widgets.Button(description=CRITERIA_APPLY, icon='filter',
                                               layout=self.LO20)
        self.filter_ddn_ndisp = widgets.Dropdown(options=['25', '50', '100', self.ALL], layout=self.LO10)
        self.filter_output = widgets.Output()
        self.filter_btn_refexp = widgets.Button(description=EXPORT_BUTTON, icon='download',
                                                layout=self.LO20)
        self.filter_out_export = widgets.Output(layout={'border': '1px solid black'})

        self.empty_list_msg()

        content = []

        # Section: Selection criteria

        section_list = []
        section_list.append(self.filter_txt_startyr)
        section_list.append(self.filter_txt_endyr)
        section_list.append(self.filter_btn_apply)
        content.append(self.section(CRITERIA_TITLE, section_list))

        # Section: Output (with apply button)

        section_list = []

        row = []
        row.append(widgets.HTML('<div style="text-align: right;">'+OUTPUT_PRE+'</div>',
                                layout=self.LO15))
        row.append(self.filter_ddn_ndisp)
        row.append(widgets.HTML('<div style="text-align: left;">' + OUTPUT_POST + '</div>',
                                layout=self.LO10))
        section_list.append(widgets.HBox(row))

        section_list.append(widgets.HBox([self.filter_output])) # NOTE Use "layout={'width': '90vw'}" to widen

        content.append(self.section(OUTPUT_TITLE, section_list))

        # Section: Export (download)

        section_list = []
        section_list.append(widgets.VBox([self.filter_btn_refexp, self.filter_out_export]))
        content.append(self.section(EXPORT_TITLE, section_list))

        return widgets.VBox(content)

    def visualize_content(self):
        '''Create widgets for visualizea tab content'''
        NOTE_TITLE = 'Note'
        NOTE_TEXT = 'The plot is based on results from the Selection tab.'
        PLOT_TITLE = 'Plot'
        PLOT_LABEL = 'Select data field'

        content = []
        content.append(self.section(NOTE_TITLE, NOTE_TEXT))

        self.plot_ddn = widgets.Dropdown(options=[self.EMPTY], value=None, disabled=True)
        self.plot_output = widgets.Output()

        section_list = []

        row = []
        row.append(widgets.HTML(value=PLOT_LABEL))
        row.append(widgets.Label(value='', layout=widgets.Layout(width='60%')))  # Cheat: spacer
        section_list.append(widgets.HBox(row))

        section_list.append(self.plot_ddn)
        section_list.append(self.plot_output)
        content.append(self.section(PLOT_TITLE, section_list))

        return widgets.VBox(content)

    def settings_content(self):
        SECTION_TITLE = 'Plot Settings'
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

        self.theme = widgets.Dropdown(description=THEME, options=THEMES)
        self.context = widgets.Dropdown(description=CONTEXT, options=CONTEXTS)
        self.fscale = widgets.FloatSlider(description=FONT_SCALE, value=1.4)
        self.spines = widgets.Checkbox(description=SPINES, value=False)
        self.gridlines = widgets.Text(description=GRIDLINES, value='--')
        self.ticks = widgets.Checkbox(description=TICKS, value=True)
        self.grid = widgets.Checkbox(description=GRID, value=False)
        self.figsize1 = widgets.FloatSlider(description=FIG_WIDTH, value=6)
        self.figsize2 = widgets.FloatSlider(description=FIG_HEIGHT, value=4.5)
        self.apply = widgets.Button(description=APPLY)

        return(self.section(SECTION_TITLE, [self.theme, self.context, self.fscale, self.spines, self.gridlines,
                                            self.ticks, self.grid, self.figsize1, self.figsize2, self.apply]))

    def update_filtered_output(self):
        """Display new data in filtered output"""

        if model.res_count < 1:
            self.output(self.EMPTY_LIST_MSG, self.filter_output)
        else:
            # Calc output line limit
            if self.filter_ddn_ndisp.value == self.ALL:
                limit = model.res_count
            else:
                limit = int(self.filter_ddn_ndisp.value)

            model.set_disp(limit=limit)
            self.output(model.results.head(limit), self.filter_output)

    def set_plot_status(self):
        """Change status of plot-related widgets based on availability of filter results"""
        if model.res_count > 0:
            self.plot_ddn.disabled = False
            self.plot_ddn.options = [self.EMPTY]+model.headers[1:]
        else:
            self.plot_ddn.disabled = True

    def get_module_export_header(self):
        '''Generate module output header for export'''
        ret = []

        for i in range(len(self.MODULE_HEADER[1])):
            pre = self.MODULE_HEADER[0][i].strip()
            title = self.MODULE_HEADER[1][i].strip()

            if not pre == '':
                title = pre + ' ' + title

            ret.append(title)

        return ret

    def output_data_link(_, output_widget, data_str):
        '''Create data URI link to download data'''

        pre = '<a download="loti.csv" target="_blank" href="data:text/csv;charset=utf-8,'
        post = '">Download</a>'

        with output_widget:
            display(widgets.HTML(pre+urllib.parse.quote(data_str)+post))

    def output(self, content, widget):
        """Reset output area with contents (text or data)"""
        widget.clear_output(wait=True)

        if isinstance(content, str):
            content = widgets.HTML(content)

        with widget:
            display(content)

    def empty_list_msg(self):
        self.output(self.EMPTY_LIST_MSG, self.filter_output)

    def plot(self):
        TITLE = 'Land-Ocean Temperature Index'

        if not self.plot_ddn.value == self.EMPTY:
            try:
                self.plot_output.clear_output(wait=True)

                with self.plot_output:
                    plt.plot(model.results[model.headers[0]], model.results[self.plot_ddn.value])
                    plt.xlabel(model.headers[0])
                    plt.ylabel(self.plot_ddn.value)
                    plt.suptitle(TITLE)
                    plt.show()

                    # Update output widget with new plot
                    plt.show()
                    logger.debug('after plt.show()')
            except Exception:
                plt.close()  # Clear any partial plot output
                logger.debug('raising exception')
                raise

    def export_link(self, filepath, output):
        """Create data URI link and add it to export output area"""
        output.clear_output()

        link = FileLink(filepath, result_html_prefix=self.EXPORT_LINK_PROMPT)

        with output:
            display(link)
