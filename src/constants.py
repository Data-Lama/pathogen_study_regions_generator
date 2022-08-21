import os
import json

# Constants

# Config Variables
# Loads config
CONFIG = {}
with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     '../config.json')) as f:
    CONFIG = json.load(f)

# Global constants from config
PIPELINE_DATA_FOLDER = CONFIG['pipeline_data_location']
GEO_DATA_FOLDER = CONFIG['geo']

# Global constants
ID = "ID"
ID_1 = "ID_1"
ID_2 = "ID_2"
SUB_ID = "SUB_ID"
DATE = "date"
VALUE = "value"
GEOMETRY = "geometry"
AREA_COL = "__polygon_area"
CLUSTER_ID = "cluster_id"

# Time resolutions
DAY = "DAY"
WEEK = "WEEK"
MONTH = "MONTH"
YEAR = "YEAR"


def isTimeResolutionValid(tr : str):
    '''
    Checks if time resolution is valid
    '''
    if tr not in [DAY, WEEK, MONTH, YEAR]:
        raise ValueError(f'Time resolution: {tr} not supported')

    return True


# Geographic Grouping constants
MAX = "max"
MIN = "min"
TOTAL = "total"
SUM = "sum"
AVERAGE = "average"

# Other grouping variables
MEAN = 'mean'
PAD = "pad"
LINEAR = "linear"


# Build grouping name
def make_grouping_name(col, grouping):
    return (f"{col}_{grouping}")


# Get grouping from column
def get_grouping(col):
    return (col.split("_")[-1])


# Data Stages constants
RAW = "raw"
SUPPLEMENTARY = "supplementary"
CACHED = "cached"

# Projection
USUAL_PROJECTION = "EPSG:4326"
MANIPULATION_PROJECTION = 'EPSG:3857'
BUFFER_PROJECTION = "EPSG:3395"

# Identation Variables
IDENT = "   "

# Testing constants
SUPPLEMENTARY_ARGS = {"Malaria": "municipalities/municipalities.shp"}

# Graph Constants
WEIGHT = "weight"
