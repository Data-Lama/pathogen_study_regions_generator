# Colombian Municipalities
from constants import GEO_DATA_FOLDER, ID
from geography.abstract.abstact_geography import AbstractGeography
import geopandas
import os


class ColombianMunicipalities(AbstractGeography):
    '''
    Geography for the municipalities of Colombia
    
    '''

    @property
    def ID(self):
        return ("colombian_municipalities")

    @property
    def name(self):
        return ("Colombian Municipalities")

    def build_geometry(self):
        df = geopandas.read_file(
            os.path.join(GEO_DATA_FOLDER, "municipalities/municipalities.shp"))
        df = df.rename(columns={"muni_id": ID})

        return (df)
