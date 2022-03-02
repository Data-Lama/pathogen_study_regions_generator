# FB mobility (matrix data source)

# Constants

from re import A
from constants import DATE, ID_2, GEOMETRY, ID, PIPELINE_DATA_FOLDER, RAW, ID_1
from data_sources.abstract.matrix_data_source import MatrixDataSource
from utils.date_functions import get_period_representative_function
from utils.facebook_functions import FB_MOVEMENT, MOVEMENT_BETWEEN_TILES, build_movement
import os
import geopandas
import pandas as pd

# Constants
__SOURCE_ID = "fb_mobility"
__NAME = "Facebook Mobility"
MOVEMENT = "movement"


class FBMobility(MatrixDataSource):
    '''
    Matrix Data Source
    '''

    def __init__(self):
        super().__init__()

    @property
    def ID(self):
        return __SOURCE_ID

    @property
    def name(self):
        return __NAME

    # Override
    def createData(self, df_geo, time_resolution):

        # Directory
        directory = os.path.join(PIPELINE_DATA_FOLDER, RAW, FB_MOVEMENT,
                                 MOVEMENT_BETWEEN_TILES)

        df_movement = build_movement(directory)

        # Agglomerates the movement
        # Creates the agglomerated movement
        df_movement = df_movement[[
            'date_time', 'start_movement_lon', 'start_movement_lat',
            'end_movement_lon', 'end_movement_lat', 'n_crisis'
        ]]

        # First Start
        df_movement = geopandas.sjoin(geopandas.GeoDataFrame(
            df_movement,
            geometry=geopandas.points_from_xy(df_movement.start_movement_lon,
                                              df_movement.start_movement_lat)),
                                      df_geo[[ID, GEOMETRY]],
                                      how='inner',
                                      op='within').rename(columns={
                                          ID: ID_1
                                      }).drop(['index_right'], axis=1)
        # Then End
        df_movement = geopandas.sjoin(geopandas.GeoDataFrame(
            df_movement,
            geometry=geopandas.points_from_xy(df_movement.end_movement_lon,
                                              df_movement.end_movement_lat)),
                                      df_geo[[ID, GEOMETRY]],
                                      how='inner',
                                      op='within').rename(columns={ID: ID_2})

        # Filters and renames
        df_movement = df_movement[['date_time', ID_1, ID_2,
                                   'n_crisis']].rename(columns={
                                       'n_crisis': MOVEMENT,
                                       "date_time": DATE
                                   })

        # Filters out geo_id not in polyong
        df_movement = df_movement[
            (df_movement[ID_1].isin(df_geo[ID].unique()))
            & (df_movement[ID_2].isin(df_geo[ID].unique()))].copy()

        # Rounds and Groups by
        df_movement[DATE] = pd.to_datetime(df_movement[DATE])
        df_movement[DATE] = df_movement.date_time.dt.round(freq='D')
        # Takes to end of period
        df_movement[DATE] = df_movement[DATE].apply(
            get_period_representative_function(time_resolution))
        df_movement = df_movement.groupby([DATE, ID_1,
                                           ID_2]).sum().reset_index()

        return df_movement
