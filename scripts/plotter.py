# plotter.py - scsa plots
# rcampbel@purdue.edu - 2020-07-14
# Based on code by A. Pendleton, November 2019

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from IPython.display import clear_output

class Plotter:

	PLOT_LIMIT		  =  100

	COLORS			  =  [
		"#63b598", "#ce7d78", "#ea9e70", "#a48a9e", "#c6e1e8", "#648177", "#0d5ac1",
		"#f205e6", "#1c0365", "#14a9ad", "#4ca2f9", "#a4e43f", "#d298e2", "#6119d0",
		"#d2737d", "#c0a43c", "#f2510e", "#651be6", "#79806e", "#61da5e", "#cd2f00",
		"#9348af", "#01ac53", "#c5a4fb", "#996635", "#b11573", "#4bb473", "#75d89e",
		"#2f3f94", "#2f7b99", "#da967d", "#34891f", "#b0d87b", "#ca4751", "#7e50a8",
		"#c4d647", "#e0eeb8", "#11dec1", "#289812", "#566ca0", "#ffdbe1", "#2f1179",
		"#935b6d", "#916988", "#513d98", "#aead3a", "#9e6d71", "#4b5bdc", "#0cd36d",
		"#250662", "#cb5bea", "#228916", "#ac3e1b", "#df514a", "#539397", "#880977",
		"#f697c1", "#ba96ce", "#679c9d", "#c6c42c", "#5d2c52", "#48b41b", "#e1cf3b",
		"#5be4f0", "#57c4d8", "#a4d17a", "#225b8e", "#be608b", "#96b00c", "#088baf",
		"#f158bf", "#e145ba", "#ee91e3", "#05d371", "#5426e0", "#4834d0", "#802234",
		"#6749e8", "#0971f0", "#8fb413", "#b2b4f0", "#c3c89d", "#c9a941", "#41d158",
		"#fb21a3", "#51aed9", "#5bb32d", "#807fbc", "#21538e", "#89d534", "#d36647",
		"#7fb411", "#0023b8", "#3b8c2a", "#986b53", "#f50422", "#983f7a", "#ea24a3",
		"#79352c", "#521250"
	]

	GENE_ID_LBL		 = 'Gene ID'

	LINE_INIT_TITLE	 = '(No filter results.)'
	LINE_PROMPT_TITLE   = '(No experiment selected.)'
	LINE_UPDATE_TITLE   = 'Updating plot...'
	LINE_PREFIX_TITLE   = 'Average Gene Expression - '
	LINE_THRESH_TOP	 = 50  # Above which need to use complex lines (dot, dash, etc)
	LINE_THRESH_MID	 = 20  # Above which need to use semi-complex lines (eg, dot)
	LINE_AXIS_TITLE_X   = 'Experimental Conditions'
	LINE_AXIS_TITLE_Y   = 'Expression'
	LINE_GRID_COLOR	 = 'whitesmoke'
	LINE_BACKGROUND	 = 'white'

	HEAT_INIT_TITLE	 = '(No filter results.)'
	HEAT_PROMPT_TITLE   = '(No experiment selected.)'
	HEAT_UPDATE_TITLE   = 'Updating plot...'
	HEAT_PREFIX_TITLE   = 'Heatmap - '
	HEAT_FONT_SIZE	  = 10
	HEAT_FIG_SIZE	   = (22,24)
	HEAT_LESS_THAN_TWO  = '(Less than two results.)'

	NET_INIT_TITLE	  = '(No filter results.)'
	NET_PROMPT_TITLE	= '(No module selected.)'
	NET_UPDATE_TITLE	= 'Updating plot...'
	NET_PREFIX_TITLE	= 'Network '
	NET_TITLE_FONT_SIZE = 16
	NET_MARKER_SIZE	 = 22
	NET_EDGE_WITH	   = 0.5
	NET_EDGE_COLOR	  = '#888'
	NET_BACKGROUND	  = 'rgba(0,0,0,0)'
	NET_HEIGHT		  = 600
	NET_WIDTH		   = 1200
	NET_CREDIT		  = "Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>"
	NET_MARGIN		  = dict(b=20,l=5,r=5,t=40)
	NET_ANNO_X		  = 0.005
	NET_ANNO_Y		  = -0.002
	NET_GENE_COLOR_EMPH = 'dodgerblue'
	NET_GENE_COLOR_NORM = 'lightgray'

	def __init__(self,ctrl):
		self.ctrl = ctrl
		init_notebook_mode(connected=False)

		# Line plot widget =========================================================

		# Create data as list of empty Scatter objects

		data		= []
		line_styles = ['solid','dot','dash']

		for i in range(self.PLOT_LIMIT):

			if   i > self.LINE_THRESH_TOP: line_style = line_styles[i % len(line_styles)  ]
			elif i > self.LINE_THRESH_MID: line_style = line_styles[i % len(line_styles)-1]
			else						 : line_style = line_styles[0]

			scatter = go.Scatter(
				x	 = []
				,y	= []
				,name = ''
				,mode = 'lines+markers'
				,line = dict(
					width  = 4
					,dash  = line_style
					,color = self.COLORS[i]
				)
			)

			data.append(scatter)

		self.line_plot = go.FigureWidget(
			data	= data
			,layout = go.Layout(
				title		 = self.LINE_INIT_TITLE
				,yaxis		= dict(
					title	  = self.LINE_AXIS_TITLE_Y
					,showgrid  = True
					,gridcolor = self.LINE_GRID_COLOR
				)
				,xaxis		= dict(
					title	  = self.LINE_AXIS_TITLE_X
					,showgrid  = True
					,gridcolor = self.LINE_GRID_COLOR
				)
				,plot_bgcolor = self.LINE_BACKGROUND
				,dragmode	 = 'select'
			)
		)

	def out_plot_msg(self,output_widget,text):
		'''Replace current plot output with message'''
		with output_widget:
			clear_output(wait=True)
			print(text)

	def limit_num_genes(self,gene_list):
		'''Truncate list of genes if needed'''
		self.ctrl.debug('Plot limit: %i max, %i genes in list' % (self.PLOT_LIMIT,len(gene_list)))
		return gene_list[:min(self.PLOT_LIMIT,len(gene_list))]

	def draw_line_plot(self,experiement,gene_list):
		'''Expression line plots for gene list generated from sample filtration steps'''
		self.line_plot.layout.title = self.LINE_UPDATE_TITLE
		gene_list				   = self.limit_num_genes(gene_list)
		avg_exp, _, _			   = self.ctrl.model.get_expression(gene_list)

		for i,gene_id in enumerate(gene_list):
			x,y = [],[]

			# Plot average expression level for each condition
			for condition in avg_exp[gene_id][experiement].keys():
				x.append(condition)
				y.append(float(avg_exp[gene_id][experiement][condition][0])) # average expression

			self.line_plot.data[i].x	 = x
			self.line_plot.data[i].y	 = y
			self.line_plot.data[i].name  = gene_id

		self.line_plot.layout.title = self.LINE_PREFIX_TITLE + experiement

	def clear_plots(self,heatmap_out_widget):
		'''Erase all data from all plot displays'''

		# Clear line plot
		for i in range(self.PLOT_LIMIT):
			self.line_plot.data[i].x	= []
			self.line_plot.data[i].y	= []
			self.line_plot.data[i].name = ''

