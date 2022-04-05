# pandas and numpy for data manipulation
import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, 
						  ColumnDataSource, Panel, 
						  FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, 
								  Tabs, CheckboxButtonGroup, 
								  TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16
from bokeh.models import CustomJS, DatePicker
import requests
# Make plot with histogram and return tab
def histogram_tab(flights):

	# Function to make a dataset for histogram based on a list of carriers
	# a minimum delay, maximum delay, and histogram bin width
	def make_plot(date):
		print("hello")
		#UAT
		#URL = "http://10.50.5.78:8551/GenericDashBoardRetrieve.ashx/ProcessRequest"
		#QC
		URL = "http://10.50.3.125:8551/GenericDashBoardRetrieve.ashx/ProcessRequest"

		data_api = {"MethodName": "ICICI_BBPS_StatusReport", "Date": date,
					"Token": "4GgYnT+iiCt+mDoSJvBRyVEOjLj6TBAOd66lrbYh4hgFnSW5DFkRohSIqOm1z7pP"}
		r = requests.post(url=URL, json=data_api)

		# extracting data in json format
		data1 = r.json()
		#print(data1)
		total_no = data1['ResultSet'][0]['TOTAL_NUMBER']
		status_check_completed = data1['ResultSet'][1]['TOTAL_NUMBER']
		status_check_pending = data1['ResultSet'][2]['TOTAL_NUMBER']
		total_success = data1['ResultSet'][3]['TOTAL_NUMBER']
		total_failure = data1['ResultSet'][4]['TOTAL_NUMBER']
		other_exception = data1['ResultSet'][5]['TOTAL_NUMBER']

		indicators = ['Total Number', 'Status Check Completed', 'Status Check Pending', 'Success', 'Failure',
				  'Other Exception']
		p = figure(x_range=indicators, plot_height=450, plot_width=800, title="ICICI BBPS Status Check Report")
		# p.vbar(x=fruits, top=[4943, 4943, 0, 4846, 0, 97], width=0.5)
		p.vbar(x=indicators, top=[total_no, status_check_completed, status_check_pending, total_success, total_failure,
							  other_exception], width=0.5)

		p.xgrid.grid_line_color = None
		p.y_range.start = 0
		return p


	
	
	
	def update(attr, old, new):
		p= make_plot(new)
		
	'''# Carriers and colors
	available_carriers = list(set(flights['name']))
	available_carriers.sort()


	airline_colors = Category20_16
	airline_colors = list(airline_colors)
	airline_colors.sort()
		
	carrier_selection = CheckboxGroup(labels=available_carriers, 
									  active = [0, 1])
	carrier_selection.on_change('active', update)
	
	binwidth_select = Slider(start = 1, end = 30, 
							 step = 1, value = 5,
							 title = 'Bin Width (min)')
	binwidth_select.on_change('value', update)
	
	range_select = RangeSlider(start = -60, end = 180, value = (-60, 120),
							   step = 5, title = 'Range of Delays (min)')
	range_select.on_change('value', update)'''

	date_picker = DatePicker(title='Select date', value="2022-03-10", min_date="2010-08-01", max_date="2025-12-30")
	date_picker.on_change('value',update)
	#date_selected = date_picker.value
	# Initial carriers and data source
	#initial_carriers = [carrier_selection.labels[i] for i in carrier_selection.active]
	
	#src = make_dataset(date_picker.value)
	p = make_plot(date_picker.value)
	
	# Put controls in a single element
	controls = WidgetBox(date_picker)
	
	# Create a row layout
	layout = row(controls, p)
	
	# Make a tab with the layout 
	tab = Panel(child=layout, title = 'Bar Graph')

	return tab
