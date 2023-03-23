# FB mobility (matrix data source)

# Constants

from constants import  PIPELINE_DATA_FOLDER, RAW
from data_sources.general.data_from_fb_mobility import FBMobilityFromFolder
from utils.facebook_functions import FB_MOVEMENT, MOVEMENT_BETWEEN_TILES_RECENT
import os

# Constants
SOURCE_ID = "fb_mobility_recent"
NAME = "Facebook Mobility Recent"


class FBMobilityRecent(FBMobilityFromFolder):
    '''
    Matrix Data Source
    '''

    def __init__(self):
        super().__init__(id=SOURCE_ID,
                         name=NAME,
                         folder=os.path.join(PIPELINE_DATA_FOLDER, RAW,
                                             FB_MOVEMENT,
                                             MOVEMENT_BETWEEN_TILES_RECENT))
