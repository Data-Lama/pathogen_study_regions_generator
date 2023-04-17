# Dengue data source

from constants import AVERAGE, SUM, WEEK
from data_sources.general.data_from_time_series_csv import DataFromTimeSeriesOfCSV
from geography.specific.colombian_municipalities import ColombianMunicipalities

# Constants
id = "dengue_sivigila_4"
name = "Dengue"


class Dengue(DataFromTimeSeriesOfCSV):
    '''
    Dengue data source
    '''

    def __init__(self):
        super().__init__(id=id,
                         name=name,
                         folder_name="dengue_cases",
                         file_name="DENGUE_filtered.csv",
                         min_year=2006,
                         max_year=2021,
                         reference_geography=ColombianMunicipalities(),
                         min_time_resolution=WEEK,
                         index_id="muni_id",
                         included_groupings=[SUM],
                         time_resolution_aggregation_function = SUM,
                         columns_of_interest=["num_cases"],
                         default_values={"num_cases": 0})
