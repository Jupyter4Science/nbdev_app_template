# view.py - User interface for scsa notebook
# rcampbel@purdue.edu - 2020-07-14

import sys
import ipywidgets as ui
import urllib
from scripts import plotter

class View:

	EMPTY_LIST_MSG = '''<br>(There's no data to display.)'''
	ALL            = 'All'
	EMPTY          = ''

	LO10 = ui.Layout(width='10%')
	LO15 = ui.Layout(width='15%')
	LO20 = ui.Layout(width='20%')
	LO25 = ui.Layout(width='25%')

	def __init__(self):
		self.tabs	= None # Main UI container

	def intro(self,model,ctrl):
		self.model = model
		self.ctrl  = ctrl

	def display(self,display_log):
		'''Build and show notebook user interface'''
		self.plotter = plotter.Plotter(self.model)
		self.build()

		if display_log:
			self.debug_output = ui.Output(layout={'border': '1px solid black'})
			display(ui.VBox([self.tabs,self.section('Log',[self.debug_output])]))
		else:
			display(self.tabs)

	def debug(self,text):
		with self.debug_output:
			print(text)

	def section(self,title,contents):
		'''Create a collapsible widget container'''

		if type(contents) == str:
			contents = [ui.HTML(value=contents)]

		ret = ui.Accordion(children=tuple([ui.VBox(contents)]))
		ret.set_title(0,title)
		return ret

	def build(self):
		'''Create user interface'''
		TITLES = ['Welcome','Data','Selection','Visualize']

		self.tabs = ui.Tab()

		# Set title for each tab
		for i in range(len(TITLES)):
			self.tabs.set_title(i,TITLES[i])

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
		USING_TEXT  = '''<p>
		In the <b>Data</b> tab above, you can review the dataset.
		In the <b>Selection</b> tab, you can search for and download data of interest.
		Once you've selected data, generate plots in the <b>Visualize</b> tab.
		</p>'''
		SOURCES_TITLE = 'Data Sources'
		SOURCES_TEXT  = '''<p>
		<b>Land-Ocean Temperature Index</b>
		<a href="https://climate.nasa.gov/vital-signs/global-temperature/" target="_blank">Global Temperature (NASA)</a>
		,
		<a href="https://data.giss.nasa.gov/gistemp/" target="_blank">GISS Surface Temperature Analysis (NASA)</a>
		</p><p>
		This site is based on data downloaded from the following site on 2020-07-14:
		<a href="https://data.giss.nasa.gov/gistemp/graphs/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.txt" target="_blank">Global Mean Estimates based on Land_and Ocean Data (NASA)</a>
		</p>'''

		content = []
		content.append(self.section(USING_TITLE  ,USING_TEXT  ))
		content.append(self.section(SOURCES_TITLE,SOURCES_TEXT))

		return ui.VBox(content)

	def data(self):
		'''Create widgets for data tab content'''
		SECTION_TITLE = 'Data'

		content = []

		# Set table format using CSS and start the HTML table
		html = '''<style>
						.data_cell {padding-right: 32px	 }
						.data_even {background   : White	}
						.data_odd  {background   : Gainsboro}
					</style><table>'''

		# Table column headers

		html += '<th class="data_cell"> </th>' # Blank header for line number

		for item in self.model.headers:
			html += '<th class="data_cell">' + item + '</th>'

		# Table items - alternate row background colors
		for i,line in enumerate(self.model.iterate_data()):

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
		content.append(self.section(SECTION_TITLE,widgets)) # TODO Constant

		return ui.VBox(content)

	def selection(self):
		'''Create widgets for selection tab content'''
		CRITERIA_TITLE = 'Selection Criteria'
		CRITERIA_LABEL = 'Temperature (C)'
		CRITERIA_APPLY = 'Search'
		OUTPUT_TITLE   = 'Results'
		OUTPUT_PRE     = 'Limit to '
		OUTPUT_POST    = 'lines'
		EXPORT_TITLE   = 'Export'
		EXPORT_BUTTON  = 'Create Download Link'

		# Create widgets
		self.filter_txt_tempc   = ui.Text(description='',value='',placeholder='')
		self.filter_btn_apply   = ui.Button(description=CRITERIA_APPLY,icon='filter',layout=self.LO20)
		self.filter_ddn_ndisp   = ui.Dropdown(options=['25','50','100',self.ALL],layout=self.LO10)
		self.filter_html_output = ui.HTML(self.EMPTY_LIST_MSG)
		self.filter_btn_refexp  = ui.Button(description=EXPORT_BUTTON,icon='download',layout=self.LO20)
		self.filter_out_export  = ui.Output(layout={'border': '1px solid black'})

		content = []

		# Section: Selection criteria

		widgets = []
		widgets.append(ui.HTML(value=CRITERIA_LABEL))
		widgets.append(self.filter_txt_tempc)
		widgets.append(self.filter_btn_apply)
		content.append(self.section(CRITERIA_TITLE,widgets))

		# Section: Output (with apply button)

		widgets = []

		row = []
		row.append(ui.HTML('<div style="text-align: right;">'+OUTPUT_PRE+'</div>',layout=self.LO15))
		row.append(self.filter_ddn_ndisp)
		row.append(ui.HTML('<div style="text-align: left;">' +OUTPUT_POST+'</div>',layout=self.LO10))
		widgets.append(ui.HBox(row))

		widgets.append(ui.HBox([self.filter_html_output],layout={'width':'90vw'}))

		content.append(self.section(OUTPUT_TITLE,widgets))

		# Section: Export (download)

		widgets = []
		widgets.append(ui.VBox([self.filter_btn_refexp,self.filter_out_export])) # TODO VBox required here?
		content.append(self.section(EXPORT_TITLE,widgets))

		return ui.VBox(content)

	def visualize(self):
		'''Create widgets for visualizea tab content'''
		NOTE_TITLE    = 'Note'
		NOTE_TEXT     = 'The plot is based on results from the Selection tab.'
		PLOT_TITLE    = 'Plot'
		PLOT_OPTIONS  = ['No Smoothing','Lowess','Both']
		PLOT_LABEL    = 'Select data fields'

		content = []
		content.append(self.section(NOTE_TITLE,NOTE_TEXT))

		self.plotex_ddn_selex_lg = ui.Dropdown(options=[self.EMPTY]+PLOT_OPTIONS,value=None,disabled=True)

		widgets = []

		row = []
		row.append(ui.HTML(value=PLOT_LABEL))
		row.append(ui.Label(value='',layout=ui.Layout(width='60%'))) # Cheat: spacer
		widgets.append(ui.HBox(row))

		widgets.append(self.plotex_ddn_selex_lg)
		widgets.append(self.plotter.line_plot) # Use widget from plotter
		content.append(self.section(PLOT_TITLE,widgets))

		return ui.VBox(content)

	def update_filtered_gene_list(self):
		'''Update filtered genes list with new data'''

		# Calc output line limit
		if self.filter_ddn_ndisp.value == self.ALL:
			limit = sys.maxsize
		else:
			limit = int(self.filter_ddn_ndisp.value)

		# CSS (style)

		output = '''<style>
					.op th {
						padding	: 3px;
						border	 : 1px solid black;
						font-size  : 6px !important;
						text-align : center;
						line-height: 14px;
						background-color: lightgray;
					}
					.op td {
						padding	: 3px;
						border	 : 1px solid black;
						font-size  : 6px !important;
						text-align : left;
						line-height: 12px;
					}
					</style>'''

		# Table start and header start
		output += '<br><table class="op"><tr><th>'+self.FILTER17_TEXT+'</th>'

		# Column headers
		for anno in self.model.anno[1:]:  # Skip first header since its for gene ID
			output += '<th class="op">'+anno+'</th>'

		output += '</tr>'

		# Build table rows
		for count,(gene_id,annos) in enumerate(self.model.filter_results_annos.items()):
			output += '<tr><td class="op">'+gene_id+'</td>'

			for key,value in annos.items():
				output += '<td class="op">'+value+'</td>'

			output += '</tr>'

			if count+1 >= limit:
				break

		output += '</table>' # End table

		self.filter_html_output.value = output  # Update UI

	def set_plot_status(self,enable):
		'''Change status of plot-related widgets based on availability of filter results'''

		self.plotter.clear_plots(self.plotex_img_dispp_hm)

		if enable:
			self.plotex_ddn_selex_lg.disabled = False
			self.plotex_ddn_selex_hm.disabled = False
			self.plotco_ddn_netw.disabled	  = False

			self.plotter.line_plot.layout.title = self.plotter.LINE_PROMPT_TITLE
			self.plotter.net_plot.layout.title  = self.plotter.NET_PROMPT_TITLE

			self.plotter.out_plot_msg(self.plotex_img_dispp_hm,self.plotter.HEAT_PROMPT_TITLE)

		else:
			self.plotex_ddn_selex_lg.disabled = True
			self.plotex_ddn_selex_hm.disabled = True
			self.plotco_ddn_netw.disabled	 = True

			self.plotter.line_plot.layout.title = self.plotter.LINE_INIT_TITLE
			self.plotter.net_plot.layout.title  = self.plotter.NET_INIT_TITLE

			self.plotter.out_plot_msg(self.plotex_img_dispp_hm,self.plotter.HEAT_INIT_TITLE)
			self.ctrl.set_module_data([self.NO_MODULE_DATA],[(None,None)])

	def get_module_export_header(self):
		'''Generate module output header for export'''
		ret = []

		for i in range(len(self.MODULE_HEADER[1])):
			pre   = self.MODULE_HEADER[0][i].strip()
			title = self.MODULE_HEADER[1][i].strip()

			if not pre == '':
				title = pre + ' ' + title

			ret.append(title)

		return ret

	def output_data_link(self,output_widget,data_str):
		'''Create data URI link to download data'''

		pre  = '<a download="scsa.csv" target="_blank" href="data:text/csv;charset=utf-8,'
		post = '">Download</a>'

		with output_widget:
			display(ui.HTML(pre+urllib.parse.quote(data_str)+post))



