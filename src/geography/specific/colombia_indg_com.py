# Colombian indigenous communities
import this
from constants import GEO_DATA_FOLDER, ID
from geography.abstract.abstact_geography import AbstractGeography
import geopandas as gpd
import os
import constants as con


class ColombianIndgCom(AbstractGeography):
    '''
    Geography for the indigenous communities of Colombia
    
    '''
    # Stable Geometry
    is_stable = True

    @property
    def ID(self):
        return ("colombian_indg_com")

    @property
    def name(self):
        return ("Colombian Indigenous Communities")

    @property
    def index(self):
        return self.__index

    def build_geometry(self):
              
        gdf = gpd.read_file(
            os.path.join(GEO_DATA_FOLDER, f"indigenous_territories/comunidades_buffer10000m.shp"))
        gdf = gdf.rename(columns={"id": ID})

        return (gdf)