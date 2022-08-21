# Colombian Grid
import this
from constants import GEO_DATA_FOLDER, ID
from geography.abstract.abstact_geography import AbstractGeography
import geopandas as gpd
import os
import constants as con


class ColombianGrid(AbstractGeography):
    '''
    Geography for the grid of Colombia
    
    '''
    # Stable Geometry
    is_stable = True
    available_resolutions = [1000, 10000]

    # Default res
    resolution = 1000

    @property
    def ID(self):
        return ("colombian_grid")

    @property
    def name(self):
        return ("Colombian grid")

    @property
    def index(self):
        return self.__index

    def set_resolution(self, resolution):
        if int(resolution) not in self.available_resolutions:
            raise Exception(f"Requested resolution of {resolution}m not available.\nPlease generate grid and save it to {GEO_DATA_FOLDER}." )

        self.resolution = resolution

    def build_geometry(self):
              
        gdf = gpd.read_file(
            os.path.join(GEO_DATA_FOLDER, f"grids/grid{self.resolution}m.shp"))
        gdf = gdf.rename(columns={"id": ID})

        return (gdf)