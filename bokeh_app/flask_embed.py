from threading import Thread

from flask import Flask, render_template
from tornado.ioloop import IOLoop

from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
from bokeh.server.server import Server
from bokeh.themes import Theme
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
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
app = Flask(__name__)
from datetime import date
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

        json_obj = json.dumps(data1)
        dict = json.loads(json_obj)
        df = pd.json_normalize(dict['ResultSet'])
        return ColumnDataSource(df)

    def make_plot(src):
        # Blank plot with correct labels
        indicators = src.data['COLUMN_NAME'].tolist()
        plot = figure(x_range=indicators, plot_height=450, plot_width=800, title="ICICI BBPS Status Check Report",
                      toolbar_location=None, tools="")
        plot.vbar(x='COLUMN_NAME', top='TOTAL_NUMBER', width=0.8, source=src)
        return plot

    def update(attr, old, new):
        new_src = make_dataset(new)
        src.data.update(new_src.data)

    date_picker = DatePicker(title='Select date', value=date.today(), min_date="2010-08-01", max_date="2025-12-30")
    date_picker.on_change('value', update)
    src = make_dataset(date_picker.value)
    p = make_plot(src)

    # Put controls in a single element
    controls = WidgetBox(date_picker)

    # Create a row layout
    row1 = row(controls, p)

    # Make a tab with the layout
    tab = Panel(child=row1, title='Histogram')
    return tab

def bkapp(doc):
    tab1 = histogram_tab()
    tabs = Tabs(tabs=[tab1])
    doc.add_root(tabs)


@app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('http://10.41.0.75:5009/bkapp')
    return render_template("embed.html", script=script, template="Flask")


def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': bkapp}, io_loop=IOLoop(), allow_websocket_origin=["10.41.0.75:8585", "10.41.0.75:5009"])
    server.start()
    server.io_loop.start()

Thread(target=bk_worker).start()


if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    app.run(port=8585)
