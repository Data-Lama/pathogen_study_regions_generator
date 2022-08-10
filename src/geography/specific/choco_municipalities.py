# Choco Municipalities
from constants import GEO_DATA_FOLDER, ID
from utils.logger import Logger
from geography.abstract.abstact_geography import AbstractGeography
import geopandas
import os
import constants as con


class ChocoMunicipalities(AbstractGeography):
    '''
    Geography for the municipalities of Choco
    
    '''
    # Stable Geometry
    is_stable = True

    @property
    def ID(self):
        return ("choco_municipalities")

    @property
    def name(self):
        return ("Choco Municipalities")

    @property
    def index(self):
        return self.__index


    def build_geometry(self):
        df = geopandas.read_file(
            os.path.join(GEO_DATA_FOLDER, "choco_munis/choco_munis.shp"))
        df = df.rename(columns={"muni_id": ID})

        return (df)
