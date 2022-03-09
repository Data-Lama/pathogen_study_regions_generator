# Data source from yearly shapefiles
import os

from constants import IDENT, DATE, PIPELINE_DATA_FOLDER, RAW, USUAL_PROJECTION, YEAR

import geopandas
import pandas as pd

from data_sources.general.data_from_time_series_shapefile import DataFromTimeSeriesOfShapefiles
from utils.logger import Logger

IDENT = IDENT


class DataFromYearlyShapefiles(DataFromTimeSeriesOfShapefiles):
    '''
    Main class for extraction for yearly shapefiles
    '''

    def __init__(self, id, name, folder_name, file_format, data_columns,
                 min_year, max_year, included_groupings):
        '''
        '''
        super().__init__(id=id,
                         name=name,
                         data_time_resolution=YEAR,
                         included_groupings=included_groupings)

        self.folder_name = folder_name
        self.data_columns = data_columns
        self.file_format = file_format
        self.min_year = min_year
        self.max_year = max_year

    # Override
    def loadTimeSeriesShapefile(self):

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
