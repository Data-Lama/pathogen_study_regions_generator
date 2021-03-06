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
                         file_name="anonymized_individual_data.csv",
                         min_year=2006,
                         max_year=2019,
                         suplementary_geography=ColombianMunicipalities(),
                         min_time_resolution=YEAR,
                         index_id="muni_id",
                         included_groupings=[SUM],
                         columns_of_interest=["num_cases"],
                         default_values={"num_cases": 0})
