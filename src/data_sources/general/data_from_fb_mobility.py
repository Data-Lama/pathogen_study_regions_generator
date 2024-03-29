# FB mobility (matrix data source)

# Constants

from re import A
from constants import DATE, ID_2, GEOMETRY, ID, ID_1, SUB_ID, USUAL_PROJECTION, isTimeResolutionValid
from data_sources.abstract.matrix_data_source import MatrixDataSource
from utils.date_functions import get_resolution_representative_function
from utils.facebook_functions import build_movement
import geopandas
import pandas as pd

from geography.abstract.abstact_geography import Geography

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
    def createData(self, geography: Geography, time_resolution: str) -> pd.DataFrame:
    
        # Checks time resolution
        isTimeResolutionValid(time_resolution)

        # Extracts geopandas
        df_geo = geography.get_geometry()
        # Directory
        directory = self.folder

        df_movement = build_movement(directory).dropna()

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
                                      how='right',
                                      predicate='within').rename(columns={
                                          ID: ID_1
                                      }).drop(['index_left'], axis=1)

        df_movement["n_crisis"] =  df_movement["n_crisis"].fillna(0)

        # Then End
        df_movement = geopandas.sjoin(
            geopandas.GeoDataFrame(df_movement,
                                   geometry=geopandas.points_from_xy(
                                       df_movement.end_movement_lon,
                                       df_movement.end_movement_lat),
                                   crs=USUAL_PROJECTION),
            df_geo[[ID, GEOMETRY]],
            how='right',
            predicate='within').rename(columns={ID: ID_2})

        df_movement["n_crisis"] =  df_movement["n_crisis"].fillna(0)

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

        # Filters out rows without time or ids
        df_movement.dropna(subset=[ID_1, ID_2, DATE], inplace=True)


        # Rounds and Groups by
        df_movement[DATE] = pd.to_datetime(df_movement[DATE])
        df_movement[DATE] = df_movement[DATE].dt.round(freq='D')
        # Takes to end of period
        df_movement[DATE] = df_movement[DATE].apply(
            get_resolution_representative_function(time_resolution))
        df_movement = df_movement.groupby([DATE, ID_1,
                                           ID_2]).sum().reset_index()


        # Extracts ids that are missing from movement matrix to fill in with 0.
        df_geo["cross_join_key"] = 0
        df_cross_join = df_geo[["ID", "cross_join_key"]].merge(df_geo[["ID", "cross_join_key"]], on="cross_join_key", how='outer')
        df_cross_join.rename(columns={"ID_x": ID_1, "ID_y": ID_2}, inplace=True)

        for d in df_movement[DATE].unique():
            df_cross_join[DATE] = d
            df_movement = df_movement.merge(df_cross_join, on=[ID_1, ID_2, DATE], how="outer").drop(columns=["cross_join_key"])
            
            df_movement.dropna(subset=[ID_1, ID_2, DATE], inplace=True)

        df_movement[MOVEMENT] = df_movement[MOVEMENT].fillna(0)


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
