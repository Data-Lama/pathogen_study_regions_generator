# Data source from yearly shapefiles
import os

from constants import DATA_SOURCE_IDENT, DATE, PIPELINE_DATA_FOLDER, RAW, USUAL_PROJECTION, WEEK

import geopandas
import pandas as pd

from data_sources.general.data_from_time_series_shapefile import DataFromTimeSeriesOfShapefiles

IDENT = DATA_SOURCE_IDENT


class DataFromWeeklyGeeExport(DataFromTimeSeriesOfShapefiles):
    '''
    Main class for extraction for yearly shapefiles
    '''

    def __init__(self, id, name, folder_name, file_name, data_columns,
                 min_year, max_year, included_groupings):
        '''
        '''
        super().__init__(id=id,
                         name=name,
                         data_time_resolution=WEEK,
                         included_groupings=included_groupings)

        self.folder_name = folder_name
        self.data_columns = data_columns
        self.file_name = file_name
        self.min_year = min_year
        self.max_year = max_year

    # Override
    def loadTimeSeriesShapefile(self):

        # Loads the shapefile
        folder_location = os.path.join(PIPELINE_DATA_FOLDER, RAW,
                                       self.folder_name)

        file_location = os.path.join(folder_location, self.file_name)

        # Reads file
        df = geopandas.read_file(file_location)
        # Projects
        df = df.to_crs(USUAL_PROJECTION)
        # Fixes Date
        df[DATE] = pd.to_datetime(df.date, unit='ms')

        df = df[self.data_columns + ['geometry']].copy()

        return (df)
