# view.py - User interface for loti notebook
# rcampbel@purdue.edu - 2020-07-14

import ipywidgets as ui
import urllib
from matplotlib import pyplot as plt
from IPython.display import display, FileLink


class View:

    EMPTY_LIST_MSG = '''<br>(There's no data to display.)'''
    ALL = 'All'
    EMPTY = ''
    FILTER_PROG = 'Searching...'
    EXPORT_LINK_PROMPT = "Click here to save file: "

    LO10 = ui.Layout(width='10%')
    LO15 = ui.Layout(width='15%')
    LO20 = ui.Layout(width='20%')
    LO25 = ui.Layout(width='25%')

    def __init__(self):
        self.tabs = None  # Main UI container

    def intro(self, model, ctrl):
        self.model = model
        self.ctrl = ctrl

    def display(self, display_log):
        '''Build and show notebook user interface'''
        self.build()

        if display_log:
            self.debug_output = ui.Output(layout={'border': '1px solid black'})
            display(ui.VBox([self.tabs, self.section('Log', [self.debug_output])]))
        else:
            display(self.tabs)

    def debug(self, text):
        with self.debug_output:
            print(text)

    def section(self, title, contents):
        '''Create a collapsible widget container'''

        if type(contents) == str:
            contents = [ui.HTML(value=contents)]

        ret = ui.Accordion(children=tuple([ui.VBox(contents)]))
        ret.set_title(0, title)
        return ret

    def build(self):
        '''Create user interface'''
        TITLES = ['Welcome', 'Data', 'Selection', 'Visualize']

        self.tabs = ui.Tab()

        # Set title for each tab
        for i in range(len(TITLES)):
            self.tabs.set_title(i, TITLES[i])

        # Build conent (widgets) for each tab
        tab_content = []
        tab_content.append(self.welcome())
        tab_content.append(self.data())
        tab_content.append(self.selection())
        tab_content.append(self.visualize())

        # Fill with content
        self.tabs.children = tuple(tab_content)

    def welcome(self):
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

        return ui.VBox(content)

    def data(self):
        '''Create widgets for data tab content'''
        SECTION_TITLE = 'Data'

        content = []

        # Set table format using CSS and start the HTML table
        html = '''<style>
                        .data_cell {padding-right: 32px     }
                        .data_even {background   : White    }
                        .data_odd  {background   : Gainsboro}
                    </style><table>'''

        # Table column headers

        html += '<th class="data_cell"> </th>'  # Blank header for line number

        for item in self.model.headers:
            html += '<th class="data_cell">' + item + '</th>'

        # Table items - alternate row background colors
        for i, line in enumerate(self.model.iterate_data()):

            if i % 2 == 0:
                html += '<tr class="data_even">'
            else:
                html += '<tr class="data_odd">'

            for item in line:
                html += '<td class="data_cell">' + str(item) + '</td>'

            html += '</tr>'

        html += '</table>'

        widgets = []
        widgets.append(ui.HTML(value=html))
        content.append(self.section(SECTION_TITLE, widgets))

        return ui.VBox(content)

    def selection(self):
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
        self.filter_txt_startyr = ui.Text(description=START_YEAR, value='', placeholder='')
        self.filter_txt_endyr = ui.Text(description=END_YEAR, value='', placeholder='')
        self.filter_btn_apply = ui.Button(description=CRITERIA_APPLY, icon='filter',
                                          layout=self.LO20)
        self.filter_ddn_ndisp = ui.Dropdown(options=['25', '50', '100', self.ALL], layout=self.LO10)
        self.filter_output = ui.Output()
        self.filter_btn_refexp = ui.Button(description=EXPORT_BUTTON, icon='download',
                                           layout=self.LO20)
        self.filter_out_export = ui.Output(layout={'border': '1px solid black'})

        self.empty_list_msg()

        content = []

        # Section: Selection criteria

        widgets = []
        widgets.append(self.filter_txt_startyr)
        widgets.append(self.filter_txt_endyr)
        widgets.append(self.filter_btn_apply)
        content.append(self.section(CRITERIA_TITLE, widgets))

        # Section: Output (with apply button)

        widgets = []

        row = []
        row.append(ui.HTML('<div style="text-align: right;">'+OUTPUT_PRE+'</div>',
                           layout=self.LO15))
        row.append(self.filter_ddn_ndisp)
        row.append(ui.HTML('<div style="text-align: left;">' + OUTPUT_POST + '</div>',
                           layout=self.LO10))
        widgets.append(ui.HBox(row))

        widgets.append(ui.HBox([self.filter_output], layout={'width': '90vw'}))

        content.append(self.section(OUTPUT_TITLE, widgets))

        # Section: Export (download)

        widgets = []
        widgets.append(ui.VBox([self.filter_btn_refexp, self.filter_out_export]))
        content.append(self.section(EXPORT_TITLE, widgets))

        return ui.VBox(content)

    def visualize(self):
        '''Create widgets for visualizea tab content'''
        NOTE_TITLE = 'Note'
        NOTE_TEXT = 'The plot is based on results from the Selection tab.'
        PLOT_TITLE = 'Plot'
        PLOT_LABEL = 'Select data field'

        content = []
        content.append(self.section(NOTE_TITLE, NOTE_TEXT))

        self.plot_ddn = ui.Dropdown(options=[self.EMPTY], value=None, disabled=True)
        self.plot_output = ui.Output()

        widgets = []

        row = []
        row.append(ui.HTML(value=PLOT_LABEL))
        row.append(ui.Label(value='', layout=ui.Layout(width='60%')))  # Cheat: spacer
        widgets.append(ui.HBox(row))

        widgets.append(self.plot_ddn)
        widgets.append(self.plot_output)
        content.append(self.section(PLOT_TITLE, widgets))

        return ui.VBox(content)

    def update_filtered_output(self):
        """Display new data in filtered output"""

        if self.model.res_count < 1:
            self.output(self.EMPTY_LIST_MSG, self.filter_output)
        else:
            # Calc output line limit
            if self.filter_ddn_ndisp.value == self.ALL:
                limit = self.model.res_count
            else:
                limit = int(self.filter_ddn_ndisp.value)

            self.model.set_disp(limit=limit)
            self.output(self.model.results.head(limit), self.filter_output)

    def set_plot_status(self):
        """Change status of plot-related widgets based on availability of filter results"""
        if self.model.res_count > 0:
            self.plot_ddn.disabled = False
            self.plot_ddn.options = [self.EMPTY]+self.model.headers[1:]
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
            display(ui.HTML(pre+urllib.parse.quote(data_str)+post))

    def output(self, content, widget):
        """Reset output area with contents (text or data)"""
        self.ctrl.logger.debug('At')
        widget.clear_output(wait=True)

        if isinstance(content, str):
            content = ui.HTML(content)

        with widget:
            display(content)

    def empty_list_msg(self):
        self.output(self.EMPTY_LIST_MSG, self.filter_output)

    def plot(self):
        if not self.plot_ddn.value == self.EMPTY:
            try:
                self.plot_output.clear_output(wait=True)

                with self.plot_output:
                    # Render plot - NOTE Assumes data is pandas datatframe TODO Abstract that?
                    self.model.results.plot(x=self.model.headers[0], y=self.plot_ddn.value,
                                            figsize=(15, 10))

                    # Update output widget with new plot
                    plt.show()
                    self.ctrl.logger.debug('after plt.show()')
            except Exception:
                plt.close()  # Clear any partial plot output
                self.logger.debug('raising exception')
                raise

    def export_link(self, filepath, output):
        """Create data URI link and add it to export output area"""
        self.ctrl.logger.debug('At')
        output.clear_output()

        link = FileLink(filepath, result_html_prefix=self.EXPORT_LINK_PROMPT)

        with output:
            display(link)
