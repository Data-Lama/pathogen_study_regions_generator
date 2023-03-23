import sys
sys.path.append('src')

import unittest
from constants import DATE, GEO_DATA_FOLDER, ID, ID_1, ID_2, MONTH, WEEK, YEAR, SUPPLEMENTARY_ARGS
import geopandas
import os
from data_sources.specific.gold_stock_price import GoldStockPrice
from data_sources.specific.malaria_cases import Malaria
from utils.logger import Logger

from geography.specific.colombian_municipalities import ColombianMunicipalities

from data_sources.specific.coca import Coca

periodicities = [WEEK, MONTH, YEAR]
shapefile_location = os.path.join(GEO_DATA_FOLDER,
                                  'municipalities/municipalities.shp')

# Loads municipalities of Colombia
muni = ColombianMunicipalities()
df_geo_ids = set(muni.get_geometry()[ID])

# Vector Data Sources
vector_data_sources = [Malaria]
matrix_data_source = []


class TestDataSources(unittest.TestCase):
    '''
    Test all the data sources
    '''

    def test_all_vector_data_sources(self):
        '''
        Test all the data sources in the array: vector_data_sources
        '''

        for data_source in vector_data_sources:

            ds = data_source()
            Logger.print_progress(f'Started: {ds.name} ({ds.ID})')
            Logger.enter_level()
            for periodocity in periodicities:
                Logger.print_progress(periodocity)
                Logger.enter_level()

                df = ds.createData(geography=muni, time_resolution=periodocity)

                # Checks Id Column
                self.assertTrue(ID in df.columns)
                self.assertEqual(set(df[ID]), df_geo_ids)

                # Checks Date Column
                self.assertTrue(DATE in df.columns)

                # Checks data columns
                self.assertTrue(len(df.columns) > 2)

                Logger.exit_level()

            Logger.exit_level()

    def test_all_matrix_data_sources(self):
        '''
        Test all the data sources in the array: matrix_data_sources
        '''

        for data_source in matrix_data_source:
            ds = data_source()
            Logger.print_progress(f'Started: {ds.name} ({ds.ID})')
            Logger.enter_level()
            for periodocity in periodicities:
                Logger.print_progress(periodocity)
                Logger.enter_level()

                df = ds.createData(geography=muni, time_resolution=periodocity)

                # Checks Id Columns
                self.assertTrue(ID_1 in df.columns)
                self.assertEqual(set(df[ID_1]).difference(df_geo_ids), set())
                #self.assertEqual(set(df[ID_1]), df_geo_ids)

                self.assertTrue(ID_2 in df.columns)
                self.assertEqual(set(df[ID_2]).difference(df_geo_ids), set())
                #self.assertEqual(set(df[ID_2]), df_geo_ids)

                # Checks Date Column
                self.assertTrue(DATE in df.columns)

                # Checks data columns
                self.assertTrue(len(df.columns) > 3)

                Logger.exit_level()

            Logger.exit_level()


if __name__ == '__main__':
    unittest.main()