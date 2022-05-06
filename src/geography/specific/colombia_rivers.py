# Colombian Rivers
from constants import GEO_DATA_FOLDER, ID
from geography.abstract.abstact_geography import AbstractGeography
import geopandas as gpd
import os
import constants as con


class ColombianRivers(AbstractGeography):
    '''
    Geography for the rivers of Colombia
    
    '''
    # Stable Geometry
    is_stable = True
    available_resolutions = [1000, 10000]

    # Default res
    resolution = 10000

    @property
    def ID(self):
        return ("colombian_rivers")

    @property
    def name(self):
        return ("Colombian rivers")

    @property
    def index(self):
        return self.__index


    def set_resolution(self, resolution):
        if int(resolution) not in self.available_resolutions:
            raise Exception(f"Requested resolution of {resolution}m not available.\nPlease generate grid and save it to {GEO_DATA_FOLDER}." )

        self.resolution = resolution

    def build_geometry(self):
        gdf = gpd.read_file(
            os.path.join(GEO_DATA_FOLDER, f"river_areas/river_areas_{self.resolution}m.shp"))
        gdf = gdf.rename(columns={"obj_id": ID})

        return (gdf)