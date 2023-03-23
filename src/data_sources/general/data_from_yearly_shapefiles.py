# Data source from yearly shapefiles
import os

from constants import IDENT, DATE, LINEAR, MEAN, PIPELINE_DATA_FOLDER, RAW, USUAL_PROJECTION, YEAR

import geopandas
import pandas as pd

from data_sources.general.data_from_geopandas import DataFromGeoPandas
from utils.logger import Logger


class DataFromYearlyShapefiles(DataFromGeoPandas):
    '''
    Main class for extraction for yearly shapefiles
    '''

    def __init__(self, 
                 id, 
                 name, 
                 folder_name, 
                 file_format, 
                 data_columns,
                 min_year, 
                 max_year, 
                 included_groupings, 
                 default_values,
                 time_resolution_aggregation_function, 
                 time_resolution_extrapolation_function= LINEAR):
        '''
        Parameters
        ----------
        id : string
            ID of the data source
        name : string
            Name of the data source
        folder_name : string
            Folder name inside the raw PIPELINE_DATA_FOLDER to search for. 
        file_format : string
            File format of teh files. Must include the variable "year" to be formated with the corresponding year.
        data_columns:
            Data columns to  extract from the source
        min_year : int
            Start year of the data source
        max_year : int
            End year of teh data source
        data_time_resolution : string
            Resolution in which the data source is in.
        included_groupings : array
            Grouping functions to be applied. See: utils.geographic_functions.overlay_over_geo for more info
        default_values : value or dict
            Value or dict indicating the default values for geometries where no value could be extracted. See: utils.geographic_functions.overlay_over_geo for more info
        time_resolution_aggregation_function : str
            How to lower the time resolution of the data source. See utils.date_functions.lower_time_resolution for more info.
        time_resolution_extrapolation_function : str
            How to increase the time resolution of the data source. See utils.date_functions.increase_time_resolution for more info.
        
        '''
        super().__init__(id=id,
                         name=name,
                         data_time_resolution=YEAR,
                         included_groupings=included_groupings,
                         default_values=default_values,
                         time_resolution_aggregation_function = time_resolution_aggregation_function,
                         time_resolution_extrapolation_function = time_resolution_extrapolation_function)

        self.folder_name = folder_name
        self.data_columns = data_columns
        self.file_format = file_format
        self.min_year = min_year
        self.max_year = max_year

    # Override
    def loadGeopandasDataFrame(self):

        all_dfs = []

        # Loads the shapefiles
        folder_location = os.path.join(PIPELINE_DATA_FOLDER, RAW,
                                       self.folder_name)
        # Iterates
        for year in range(self.min_year, self.max_year + 1):

            file_location = os.path.join(folder_location,
                                         self.file_format.format(year=year))

            if not os.path.isfile(file_location):
                Logger.print_progress(f"No file found for year {year}")
                continue

            # Reads file
            df = geopandas.read_file(file_location)
            df = df.to_crs(USUAL_PROJECTION)

            df = df[self.data_columns + ['geometry']].copy()

            df[DATE] = pd.to_datetime(f"{year}-12-31")

            all_dfs.append(df)

        # Joins into single one
        df = pd.concat(all_dfs, ignore_index=True)

        return (df)
