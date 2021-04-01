# controller.py - Central logic for scsa notebook
# rcampbel@purdue.edu - 2020-07-14

import os

import logging
import traceback

# Avoids warning: "numpy.dtype size changed, may indicate binary incompatibility"
import warnings
warnings.filterwarnings('ignore')

class Controller(logging.Handler):

	VALUE = 'value' # for observe calls

	def __init__(self,log=False,debug=False):
		self.display_log   = log
		self.debugging     = debug # Add debug info to log?
		self.debug_buffer  = []
		self.display_ready = False

		log_level = logging.DEBUG

		logging.Handler.__init__(self)
		self.logger = logging.getLogger(__name__)
		self.setFormatter(logging.Formatter('%(message)s - %(funcName)s(),%(filename)s:%(lineno)d'))
		self.logger.addHandler(self)

		# Must set log level for logger AND handler (Controller)
		self.logger.setLevel(log_level)
		self.setLevel(log_level)

	def intro(self,model,view):
		'''Introduce MVC modules to each other'''
		self.model = model
		self.view  = view

	def emit(self,message):
		'''Pass new log msg to view for display'''
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

			# Connect UI widgets to callback methods ("cb_...").
			# These methods will be run when user changes widget.

			# ________ Widget ___________________ _____________Method to call ___________________
			# self.view.filter_btn_apply.on_click(  self.cb_apply_filter)
			# self.view.filter_ddn_ndisp.observe(   self.cb_ndisp_changed,self.VALUE)
			# self.view.filter_btn_refexp.on_click( self.cb_fill_results_export)
			# self.view.viz_ddn_plot_type.observe(  self.cb_plot_type_selected,self.VALUE)
			# self.view.data_ddn_src.observe(       self.cb_data_source_selected,self.VALUE)
		except:
			self.logger.debug('EXCEPTION\n'+traceback.format_exc())
			raise

	def cb_fill_results_export(self,change):
		# Generate output file
		self.view.filter_out_export.clear_output()

		if self.model.filter_results:
			self.view.output_data_link(self.view.filter_out_export,self.model.write_filtered_data())

	def cb_fill_module_export(self,change):
		# Generate output file
		self.view.plotco_out_export.clear_output()

		if self.model.filter_results:
			self.view.output_data_link(self.view.plotco_out_export,self.model.module_download_data)

	def cb_apply_filter(self,change):
		'''React to apply filter button press'''

		self.view.filter_html_output.value = self.view.FILTER_PROG

		# Clear export widgets
		self.view.filter_out_export.clear_output()
		self.view.plotco_out_export.clear_output()

		# Reset some plot-control widgets (others done in set_plot_status())
		self.view.plotex_ddn_selex_lg.value = self.view.EMPTY
		self.view.plotex_ddn_selex_hm.value = self.view.EMPTY
		self.view.plotco_ddn_netw.value	 = self.view.EMPTY
		self.set_module_data([''],[(None,None)])
		self.model.clear_module_download()

		# Get IDs from UI
		gene_ids   = self.parse(self.view.filter_txt_gene.value)
		func_ids   = self.parse(self.view.filter_txt_func.value)
		self.debug('Preped gene IDs:'+str(gene_ids))
		self.debug('Preped func IDs:'+str(func_ids))

		# Translate to native.
		target_ids = self.model.translate_genes(gene_ids,func_ids)
		self.debug('Searching for '+str(len(target_ids))+' IDs; first few: '+str(target_ids[:10]))

		perform_search = True

		if not target_ids:

			if len(gene_ids) > 0 or len(func_ids) > 0: # Did user specify gene(s) or funtion(s)?
				perform_search = False
				self.debug('Translation failed.')
			else:
				self.view.filter_html_output.value = self.view.FILTER_PROG_ALL
				self.debug('WARNING: Considering ALL genes.')

		self.model.clear_filter_results() # New search attempt so reset

		if perform_search: # Either terms were left empty (user wants full results) or at least one Sevir ID is available

			# Get thresholds from from UI
			tpm_thresh  = float(self.view.filter_txt_tpm.value )
			pval_thresh = float(self.view.filter_txt_pval.value)
			fdr_thresh  = float(self.view.filter_txt_fdr.value )

			# Search for valid data, (results stored in model)
			self.model.search(target_ids,tpm_thresh,pval_thresh,fdr_thresh)

			# Get annotation data (stored in model) for search results
			self.model.add_annos()

		# Refresh output widgets
		self.refresh_filter_output()

	def cb_ndisp_changed(self,change):
		self.refresh_filter_output()

	def cb_refresh_filter_output(self):
		# Enable or disable controls based on filter results
		if self.model.filter_results:
			self.view.update_filtered_gene_list()	# Update output table in filter tab
			self.view.set_plot_status(enable=True)
		else:
			self.view.filter_html_output.value = self.view.EMPTY_LIST_MSG
			self.view.filter_btn_downd.update()  # Disable download
			self.view.set_plot_status(enable=False)

	def linegraph_experiment_selected(self,change):
		'''React to experiment selection for line graph'''
		experiment = change['owner'].value

		if experiment != self.view.EMPTY:
			gene_list   = list(self.model.filter_results.keys())
			self.plotter.draw_line_plot(experiment,gene_list)

