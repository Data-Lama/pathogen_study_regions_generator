# FB mobility (matrix data source)

# Constants

from re import A
from constants import DATE, ID_2, GEOMETRY, ID, ID_1, SUB_ID, USUAL_PROJECTION, isTimeResolutionValid
from data_sources.abstract.matrix_data_source import MatrixDataSource
from utils.date_functions import get_period_representative_function
from utils.facebook_functions import build_movement
import geopandas
import pandas as pd

# Constants
MOVEMENT = "movement"


class FBMobilityFromFolder(MatrixDataSource):
    '''
    Matrix Data Source
    '''

    def __init__(self, id, name, folder):
        super().__init__()
        self.__id = id
        self.__name = name
        self.folder = folder

    @property
    def ID(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    # Override
    def createData(self, df_geo, time_resolution):

        # Checks time resolution
        isTimeResolutionValid(time_resolution)

        # Directory
        directory = self.folder

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
                                              df_movement.start_movement_lat),
            crs=USUAL_PROJECTION),
                                      df_geo[[ID, GEOMETRY]],
                                      how='inner',
                                      predicate='within').rename(columns={
                                          ID: ID_1
                                      }).drop(['index_right'], axis=1)
        # Then End
        df_movement = geopandas.sjoin(
            geopandas.GeoDataFrame(df_movement,
                                   geometry=geopandas.points_from_xy(
                                       df_movement.end_movement_lon,
                                       df_movement.end_movement_lat),
                                   crs=USUAL_PROJECTION),
            df_geo[[ID, GEOMETRY]],
            how='inner',
            predicate='within').rename(columns={ID: ID_2})

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
        df_movement[DATE] = df_movement[DATE].dt.round(freq='D')
        # Takes to end of period
        df_movement[DATE] = df_movement[DATE].apply(
            get_period_representative_function(time_resolution))
        df_movement = df_movement.groupby([DATE, ID_1,
                                           ID_2]).sum().reset_index()

        return df_movement

    def createDataFromCachedSubGeography(self, time_resolution, sub_geography,
                                         df_map):

        # Checks time resolution
        isTimeResolutionValid(time_resolution)

        # Gets the data from the sub_geography
        df = self.get_data(sub_geography, time_resolution)

        # Maps the ids
        # id 1
        df.rename(columns={ID_1: SUB_ID}, inplace=True)
        df = df.merge(df_map).rename(columns={ID: ID_1})
        df.drop(SUB_ID, axis=1, inplace=True)
        # Id 2
        df.rename(columns={ID_2: SUB_ID}, inplace=True)
        df = df.merge(df_map).rename(columns={ID: ID_2})
        df.drop(SUB_ID, axis=1, inplace=True)

        # Agglomerates
        df_final = df.groupby([ID_1, ID_2, DATE]).sum().reset_index()

        return (df_final)
