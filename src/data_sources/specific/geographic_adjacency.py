# Geographic Adjacency
# Constants

from re import A
from constants import BUFFER_PROJECTION, DATE, ID_2, GEOMETRY, ID, ID_1
from data_sources.abstract.matrix_data_source import MatrixDataSource
from utils.date_functions import  get_today, take_to_resolution_representative
import os
import geopandas
import pandas as pd

from geography.abstract.abstact_geography import Geography

# Constants
SOURCE_ID = "geographic_adjacency"
NAME = "Geographic Adjacency"
ADJACENCY = "adjacency"


class FBMobility(MatrixDataSource):
    '''
    Matrix Data Source
    '''

    def __init__(self):
        super().__init__()

    @property
    def ID(self):
        return SOURCE_ID

    @property
    def name(self):
        return NAME

    # Override
    def createData(self, geography: Geography, time_resolution: str) -> pd.DataFrame:

        # Extracts geopandas
        df_geo = geography.get_geometry()

        # Global matrix
        df_matrix = df_geo[[ID]].drop_duplicates().merge(
            df_geo[[ID]].drop_duplicates(), how='cross').rename(columns={
                f"{ID}_x": ID_1,
                f"{ID}_y": ID_2
            })

        # Buffers
        df_geo_temp = df_geo.copy()
        df_geo_temp.geometry = df_geo_temp.geometry.to_crs(
            BUFFER_PROJECTION).buffer(50)
        # Crosses
        df_cross = geopandas.sjoin(df_geo_temp,
                                   df_geo_temp).reset_index().drop(GEOMETRY,
                                                                   axis=1)
        df_cross.rename(columns={
            f"{ID}_left": ID_1,
            f"{ID}_right": ID_2
        },
                        inplace=True)
        # Filters
        df_cross = df_cross[[ID_1, ID_2]].copy()
        df_cross[ADJACENCY] = 1

        df_matrix = df_matrix.merge(df_cross, how='left').fillna(0)

        # Adds date
        df_matrix[DATE] = take_to_resolution_representative(
            get_today(), time_resolution)

        df_matrix = df_matrix[[DATE, ID_1, ID_2, ADJACENCY]].copy()

        return df_matrix
