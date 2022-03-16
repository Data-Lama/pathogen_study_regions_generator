# Colombian Municipalities
from constants import GEO_DATA_FOLDER, ID
from geography.abstract.abstact_geography import AbstractGeography
import geopandas
import os
import constants as con


class ColombianMunicipalities(AbstractGeography):
    '''
    Geography for the municipalities of Colombia
    
    '''

    def __init__(self,
                index=con.ID):

        super().__init__()
        self.__index = index


    @property
    def ID(self):
        return ("colombian_municipalities")

    @property
    def name(self):
        return ("Colombian Municipalities")

    @property
    def index(self):
        return self.__index

    def build_geometry(self):
        df = geopandas.read_file(
            os.path.join(GEO_DATA_FOLDER, "municipalities/municipalities.shp"))
        df = df.rename(columns={"muni_id": ID})

        return (df)
