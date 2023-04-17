# Malaria data source

from constants import SUM, TOTAL, DAY, WEEK, MONTH, YEAR
from data_sources.general.data_from_time_series_csv import DataFromTimeSeriesOfCSV
from geography.specific.colombian_municipalities import ColombianMunicipalities

# Constants
id = "malaria"
name = "Malaria"


class Malaria(DataFromTimeSeriesOfCSV):
    '''
    malaria data source
    '''

    def __init__(self):
        super().__init__(id=id,
                         name=name,
                         folder_name="malaria_cases",
                         file_name="MALARIA_filtered.csv",
                         min_year=2006,
                         max_year=2021,
                         reference_geography=ColombianMunicipalities(),
                         min_time_resolution=YEAR,
                         index_id="muni_id",
                         included_groupings=[SUM],
                         time_resolution_aggregation_function = SUM,
                         columns_of_interest=["num_cases"],
                         default_values={"num_cases": 0})
