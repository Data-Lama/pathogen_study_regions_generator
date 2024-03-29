import os
import pandas as pd
import geopandas as gpd

from constants import DATE, ID_2, ID, PIPELINE_DATA_FOLDER, RAW, ID_1, SUB_ID, isTimeResolutionValid
from data_sources.abstract.matrix_data_source import MatrixDataSource
from utils.date_functions import get_resolution_representative_function
from utils import distance_functions

from geography.abstract.abstact_geography import Geography


class IBD(MatrixDataSource):
    '''
    Matrix Data Source
    '''

    def __init__(self):
        super().__init__()
    
    distance = 'min'

    @property
    def ID(self):
        return f"ibd-{self.distance}"

    @property
    def name(self):
        return "Identity by descent"

    def set_distance(self, distance):
        '''
        Distance to collapse IBD matrix. One of:
            - min
            - max
            - mean
            - hausdorff
        '''
        self.distance = distance

    # Override
    def createData(self, geography: Geography, time_resolution: str) -> pd.DataFrame:

        # Extracts geopandas
        df_geo = geography.get_geometry()

        # Checks time resolution
        isTimeResolutionValid(time_resolution)

        # Data
        data_path = os.path.join(PIPELINE_DATA_FOLDER, RAW, 'ibd', 'ibd_muni.csv')
        muni_path = os.path.join(PIPELINE_DATA_FOLDER, RAW, 'geo', 'municipalities', 'municipalities.shp')

        df = pd.read_csv(data_path, parse_dates=["date_1", "date_2"], sep='\t')
        gdf_muni = gpd.read_file(muni_path)

        # Takes to end of period
        df["date_1"] = df["date_1"].apply(
            get_resolution_representative_function(time_resolution))

        df["date_2"] = df["date_2"].apply(
            get_resolution_representative_function(time_resolution))

        # Drop rows where time resolution doesn't match
        df = df[df["date_1"] == df["date_2"]]
        df.drop(columns=["date_2"], inplace=True)
        df.rename(columns={"date_1": DATE}, inplace=True)

        # Filters out geo_id not in polyong
        df = df[
            (df[ID_1].isin(df_geo[ID].unique()))
            & (df[ID_2].isin(df_geo[ID].unique()))].copy()

        # Group by date id1, id2, and date to apply desired distance function
        if self.distance == 'hausdorff':
            df = df.groupby(DATE).apply(distance_functions.hausdorff).reset_index().drop(columns=["level_1"])
        else:
            df = df.groupby([DATE, ID_1, ID_2]).apply(self.distance).reset_index()

        
        return df

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