# Data source from yearly shapefiles
import os
from this import d

from constants import CONFIG, DATA_SOURCE_IDENT, DATE, DENSITY, ID, MANIPULATION_PROJECTION, MAX, MIN, PIPELINE_DATA_FOLDER, RAW, TOTAL, USUAL_PROJECTION, isTimeResolutionValid
from data_sources.data_source import DataSource

import geopandas
import pandas as pd

from utils.date_functions import get_dates_between_years_by_resolution

IDENT = DATA_SOURCE_IDENT


class DataFromYearlyShapefiles(DataSource):
    '''
    Main class for extraction for yearly shapefiles
    '''

    def __init__(self,
                 ID,
                 name,
                 folder_name,
                 file_format,
                 data_columns,
                 min_year,
                 max_year,
                 normalize=None,
                 included_groupings=[TOTAL]):
        '''
        '''
        super().__init__()
        self.__ID = ID
        self.__name = name
        self.folder_name = folder_name
        self.data_columns = data_columns
        self.file_format = file_format
        self.min_year = min_year
        self.max_year = max_year

        # Optionasl properties
        self.normalize = normalize
        self.included_groupings = included_groupings

    @property
    def ID(self):
        return self.__ID

    @property
    def name(self):
        return self.__name

    # Override
    def createData(self, df_geo, time_resolution):

        # Checks time resolution
        isTimeResolutionValid(time_resolution)

        all_dfs = []

        # Loads the shapefiles
        folder_location = os.path.join(PIPELINE_DATA_FOLDER, RAW,
                                       self.folder_name)
        # Iterates
        for year in range(self.min_year, self.max_year + 1):

            print(f"{IDENT}Processing year: {year}")
            file_location = os.path.join(folder_location,
                                         self.file_format.format(year=year))

            if not os.path.isfile(file_location):
                print(f"{IDENT}   No file found for year {year}")
                continue

            # Reads file
            df = geopandas.read_file(file_location)
            df = df.to_crs(USUAL_PROJECTION)

            df = df[self.data_columns + ['geometry']].copy()

            # Checks if normalize
            if self.normalize is not None:
                df[self.data_columns] = df[self.data_columns].divide(
                    df[self.data_columns].max()) * self.normalize

            # Overlays over the desired Geography
            df_overlayed = geopandas.overlay(df_geo[[ID, 'geometry']],
                                             df,
                                             how='intersection')

            df_overlayed = df_overlayed.groupby(ID).apply(
                construct_values_extraction(self.included_groupings,
                                            df_geo)).reset_index().drop(
                                                'level_1', axis=1)

            df_overlayed['year'] = year

            all_dfs.append(df_overlayed)

        # Joins into single one
        df = pd.concat(all_dfs, ignore_index=True)

        # Extracts the dates
        all_dates = get_dates_between_years_by_resolution(
            min_year=self.min_year,
            max_year=self.max_year,
            time_resolution=time_resolution)

        # Converts to df
        df_dates = pd.DataFrame({DATE: all_dates})
        df_dates
        df_dates['year'] = df_dates[DATE].dt.year

        # Merges
        df = df.merge(df_dates)
        df.drop('year', inplace=True, axis=1)

        # Orders columns
        return (df[[ID, DATE] +
                   df.columns.difference([ID, DATE]).values.tolist()].copy())


def construct_values_extraction(included_groupings, df_geo):

    # Response
    def extract_values(df):

        geo_id = df.iloc[0][ID]
        area = df_geo[df_geo[ID] == geo_id].geometry.to_crs(
            MANIPULATION_PROJECTION).area.values[0]

        response = {}
        for col in df.columns:
            if col in [ID, 'geometry']:
                continue

            if MAX in included_groupings:
                response[f"{col}_{MAX}"] = df[col].max()
            if MIN in included_groupings:
                response[f"{col}_{MIN}"] = df[col].min()
            if TOTAL in included_groupings:
                response[f"{col}_{TOTAL}"] = (
                    df[col] *
                    df.geometry.to_crs(MANIPULATION_PROJECTION).area).sum()
            if DENSITY in included_groupings:
                response[f"{col}_{DENSITY}"] = (df[col] * df.geometry.to_crs(
                    MANIPULATION_PROJECTION).area).sum() / area

            return (pd.DataFrame([response]))

    return extract_values
