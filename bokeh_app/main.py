# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs


# Each tab is drawn by one script
from scripts.bargraph import histogram_tab
from scripts.density import density_tab
from scripts.table import table_tab
from scripts.draw_map import map_tab
from scripts.routes import route_tab
import requests
import json

# Using included state data from Bokeh for map
from bokeh.sampledata.us_states import data as states

'''URL = "http://172.17.17.201:8088/GenericDashBoardRetrieve.ashx/ProcessRequest"
data_api = {"MethodName":"ICICI_BBPS_StatusReport","Date":"2022-03-23","Token":"4GgYnT+iiCt+mDoSJvBRyVEOjLj6TBAOd66lrbYh4hgFnSW5DFkRohSIqOm1z7pP"}
r = requests.post(url=URL, json=data_api)
print(r)
# extracting data in json format
data1 = r.json()
json_obj = json.dumps(data1)
dict = json.loads(json_obj)
flights = pd.json_normalize(dict['ResultSet'])
print(flights)

# Read data into dataframes
#flights = pd.read_csv(join(dirname(__file__), 'data', 'flights.csv'),
#	                                          index_col=0).dropna()
print(type(flights))
# Formatted Flight Delay Data for map
#map_data = pd.read_csv(join(dirname(__file__), 'data', 'flights_map.csv'),
#                            header=[0,1], index_col=0)'''

# Create each of the tabs
tab1 = histogram_tab()
#tab2 = density_tab(flights)
#tab3 = table_tab(flights)
#tab4 = map_tab(map_data, states)
#tab5 = route_tab(flights)

# Put all the tabs into one application
#tabs = Tabs(tabs = [tab1, tab2, tab3, tab4, tab5])
tabs = Tabs(tabs = [tab1])
# Put the tabs in the current document for display
curdoc().add_root(tabs)


