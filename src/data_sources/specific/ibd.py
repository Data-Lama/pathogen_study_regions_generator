import os
import pandas as pd
import geopandas as gpd

from constants import DATE, ID_2, GEOMETRY, ID, PIPELINE_DATA_FOLDER, RAW, ID_1, SUB_ID, USUAL_PROJECTION, isTimeResolutionValid
from data_sources.abstract.matrix_data_source import MatrixDataSource
from utils.date_functions import get_period_representative_function


class IBD(MatrixDataSource):
    '''
    Matrix Data Source
    '''

    def __init__(self):
        super().__init__()

        self.ibd_threshold = 0.9

    @property
    def ID(self):
        return SOURCE_ID

    @property
    def name(self):
        return NAME

    def set_ibd_threshold(self, ibd_threshold):
        self.ibd_threshold = ibd_threshold



    # Override
    def createData(self, df_geo, time_resolution):

        # Checks time resolution
        isTimeResolutionValid(time_resolution)

        # Data
        data_path = os.path.join(PIPELINE_DATA_FOLDER, RAW, 'ibd', 'ibd_muni.csv')
        muni_path = os.path.join(PIPELINE_DATA_FOLDER, RAW, 'geo', 'municipalities', 'municipalities.shp')

        df = pd.read_csv(data_path, parse_dates=["date_1", "date_2"], sep='\t')
        gdf_muni = gpd.read_file(muni_path)

        # Takes to end of period
        df["date_1"] = df["date_1"].apply(
            get_period_representative_function(time_resolution))

        df["date_2"] = df["date_2"].apply(
            get_period_representative_function(time_resolution))

        # Drop rows where time resolution doesn't match
        df = df[df["date_1"] == df["date_2"]]
        df.drop(columns=["date_2"], inplace=True)
        df.rename(columns={"date_1": "date"}, inplace=True)

        # Group by date id1, id2, and date to get min
        df = df.groupby(["date", "ID_1", "ID_2"]).min().reset_index()

        # Adds geometry
        # First ID_1
        gdf_ibd_1 = gpd.GeoDataFrame(gdf_muni.merge(df, left_on="muni_id", right_on=ID_1).dropna().drop(columns=["muni_id"]), 
                geometry='geometry', crs=USUAL_PROJECTION)
        gdf_ibd_1 = gpd.sjoin(gdf_ibd_1, df_geo[[ID, GEOMETRY]], how='left', predicate='contains')

        # Then ID_2
        gdf_ibd_2 = gpd.GeoDataFrame(gdf_muni.merge(df, left_on="muni_id", right_on=ID_2).dropna().drop(columns=["muni_id"]), 
                geometry='geometry', crs=USUAL_PROJECTION).dropna()                
        gdf_ibd_2 = gpd.sjoin(gdf_ibd_2, df_geo[[ID, GEOMETRY]], how='left', predicate='contains').drop(['index_right', ID], axis=1)

        # Merge gdf and merge geometries by union. Resulting geometry is the union of the corresponding polygons
        gdf_ibd = gdf_ibd_1[["geometry", "date", "ID_1", "ID_2"]].merge(gdf_ibd_2, on=["date", "ID_1", "ID_2"])        

        # Transform geomtry into a grouping
        gdf_ibd["geometry"] = gdf_ibd.apply(lambda x: gpd.GeoSeries([x["geometry_x"], x["geometry_y"]]).unary_union, axis=1)
        gdf_ibd.drop(columns=["geometry_x", "geometry_y"], inplace=True)
        
        gdf_ibd = gpd.GeoDataFrame(gdf_ibd, geometry='geometry')
        return gdf_ibd

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