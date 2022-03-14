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
DATE = "date"
VALUE = "value"
GEOMETRY = "geometry"
CLUSTER_ID = "cluster_id"

# Time resolutions
DAY = "DAY"
WEEK = "WEEK"
MONTH = "MONTH"
YEAR = "YEAR"


def isTimeResolutionValid(tr):
    if tr not in [DAY, WEEK, MONTH, YEAR]:
        raise ValueError(f'Time resolution: {tr} not supported')

    return True


# Geographic Grouping constants
MAX = "max"
MIN = "min"
TOTAL = "total"
AVERAGE = "average"

# Data Stages constants
RAW = "raw"
SUPPLEMENTARY = "supplementary"

# Projection
USUAL_PROJECTION = "EPSG:4326"
MANIPULATION_PROJECTION = 'EPSG:3857'

# Identation Variables
IDENT = "   "

# Testing constants
SUPPLEMENTARY_ARGS = {"Malaria": "municipalities/municipalities.shp"}
