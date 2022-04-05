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
import requests,json
from datetime import date

# Make plot with histogram and return tab
def histogram_tab():
    # Function to make a dataset for histogram based on a list of carriers
    # a minimum delay, maximum delay, and histogram bin width
    def make_dataset(date):
        # QC
        URL = "http://10.50.3.125:8551/GenericDashBoardRetrieve.ashx/ProcessRequest"

        data_api = {"MethodName": "ICICI_BBPS_StatusReport", "Date": date,
                    "Token": "4GgYnT+iiCt+mDoSJvBRyVEOjLj6TBAOd66lrbYh4hgFnSW5DFkRohSIqOm1z7pP"}
        r = requests.post(url=URL, json=data_api)

        # extracting data in json format
        data1 = r.json()
        print(data1)
        '''total_no = data1['ResultSet'][0]['TOTAL_NUMBER']
        status_check_completed = data1['ResultSet'][1]['TOTAL_NUMBER']
        status_check_pending = data1['ResultSet'][2]['TOTAL_NUMBER']
        total_success = data1['ResultSet'][3]['TOTAL_NUMBER']
        total_failure = data1['ResultSet'][4]['TOTAL_NUMBER']
        other_exception = data1['ResultSet'][5]['TOTAL_NUMBER']'''
        json_obj = json.dumps(data1)
        dict = json.loads(json_obj)
        df = pd.json_normalize(dict['ResultSet'])
        return ColumnDataSource(df)

    def style(p):
        # Title
        p.title.align = 'center'
        p.title.text_font_size = '20pt'
        p.title.text_font = 'serif'

        # Axis titles
        p.xaxis.axis_label_text_font_size = '14pt'
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_size = '14pt'
        p.yaxis.axis_label_text_font_style = 'bold'

        # Tick labels
        p.xaxis.major_label_text_font_size = '12pt'
        p.yaxis.major_label_text_font_size = '12pt'

        return p

    def make_plot(src):
        # Blank plot with correct labels
        print(src.data)
        indicators = list(src.data['COLUMN_NAME'])
        print(indicators)
        values = list(src.data['TOTAL_NUMBER'])
        print(values)
        p = figure(x_range=indicators, plot_height=450, plot_width=800, title="ICICI BBPS Status Check Report")
        p.vbar(x=indicators, top=values, width=0.5)

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        return p


    def update(attr, old, new):
        #carriers_to_plot = [carrier_selection.labels[i] for i in carrier_selection.active]
        print(new)
        new_src = make_dataset(new)
        src.data.update(new_src.data)
        print("new",src.data)


    date_picker = DatePicker(title='Select date', value=date.today(), min_date="2010-08-01", max_date="2025-12-30")


    # Initial carriers and data source
    #initial_carriers = [carrier_selection.labels[i] for i in carrier_selection.active]

    src = make_dataset(date_picker.value)
    p = make_plot(src)

    # Put controls in a single element
    controls = WidgetBox(date_picker)

    # Create a row layout
    layout = row(controls, p)

    # Make a tab with the layout
    tab = Panel(child=layout, title='Histogram')
    date_picker.on_change('value', update)

    return tab
