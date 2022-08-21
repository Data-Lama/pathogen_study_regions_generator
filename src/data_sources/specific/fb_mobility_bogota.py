# FB mobility (matrix data source)

# Constants

from re import A
from constants import DATE, ID_2, GEOMETRY, ID, PIPELINE_DATA_FOLDER, RAW, ID_1, SUB_ID, USUAL_PROJECTION, isTimeResolutionValid
from data_sources.abstract.matrix_data_source import MatrixDataSource
from data_sources.general.data_from_fb_mobility import FBMobilityFromFolder
from utils.date_functions import get_resolution_representative_function
from utils.facebook_functions import FB_MOVEMENT, MOVEMENT_BETWEEN_TILES, build_movement
import os
import geopandas
import pandas as pd

# Constants
SOURCE_ID = "fb_mobility_bogota"
NAME = "Facebook Mobility Bogota"


class FBMobilityBogota(FBMobilityFromFolder):
    '''
    Matrix Data Source
    '''

    def __init__(self):
        super().__init__(id=SOURCE_ID,
                         name=NAME,
                         folder=os.path.join(
                             PIPELINE_DATA_FOLDER, RAW, FB_MOVEMENT,
                             "movement_between_tiles_bogota_recent"))
