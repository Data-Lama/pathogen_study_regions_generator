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

# Global constants
ID = "ID"
DATE = "date"

# Time resolutions
WEEK = "WEEK"
MONTH = "MONTH"
YEAR = "YEAR"


def isTimeResolutionValid(tr):
    if tr not in [WEEK, MONTH, YEAR]:
        raise ValueError(f'Time resolution: {tr} not supported')

    return True


# Grouping constants
MAX = "max"
MIN = "min"
TOTAL = "total"
DENSITY = "density"

# Data Stages constants
RAW = "raw"

# Projection
USUAL_PROJECTION = "EPSG:4326"
MANIPULATION_PROJECTION = 'EPSG:3857'

# Identation Variables
DATA_SOURCE_IDENT = "      "