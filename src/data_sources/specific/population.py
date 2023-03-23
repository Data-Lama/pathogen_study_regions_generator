# Population data source

from constants import SUM, YEAR
from data_sources.general.data_from_time_series_csv import DataFromTimeSeriesOfCSV
from geography.specific.colombian_municipalities import ColombianMunicipalities

# Constants
id = "population"
name = "Population"


class Population(DataFromTimeSeriesOfCSV):
    '''
    Population data source
    '''

    def __init__(self):
        super().__init__(id=id,
                         name=name,
                         folder_name="dane",
                         file_name="population.csv",
                         min_year=1985,
                         max_year=2035,
                         reference_geography=ColombianMunicipalities(),
                         min_time_resolution=YEAR,
                         index_id="muni_id",
                         included_groupings=[SUM],
                         time_resolution_aggregation_function = SUM,
                         columns_of_interest=["urban","rural","total"],
                         default_values=0)
