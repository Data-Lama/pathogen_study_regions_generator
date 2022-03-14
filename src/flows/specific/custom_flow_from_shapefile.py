# Test Flow

from clusterers.specific.identity_clusterer import IdentityClusterer
from constants import ID, WEEK
from embedders.specific.identity_embedder import IdentityEmbbeder
from flows.abstract.abstract_flow import AbstractFlow

import geopandas


class CustomFlowFromShapefile(AbstractFlow):

    def __init__(self,
                 ID,
                 name,
                 time_resolution,
                 shapefile_location,
                 id_column,
                 vector_data_sources=[],
                 matrix_data_sources=[],
                 embedder=IdentityEmbbeder(),
                 clusterer=IdentityClusterer()):
        super().__init__()

        # Abstract
        self.__ID = ID
        self.__name = name
        self.__time_resolution = time_resolution
        self.__vector_data_sources = vector_data_sources
        self.__matrix_data_sources = matrix_data_sources
        self.__embedder = embedder
        self.__clusterer = clusterer

        # Specific
        self.shapefile_location = shapefile_location
        self.id_column = id_column

    @property
    def ID(self):
        return (self.__ID)

    @property
    def name(self):
        return (self.__name)

    @property
    def time_resolution(self):
        return (self.__time_resolution)

    @property
    def vector_data_sources(self):
        return (self.__vector_data_sources)

    @property
    def matrix_data_sources(self):
        return (self.__matrix_data_sources)

    @property
    def embedder(self):
        return (self.__embedder)

    @property
    def clusterer(self):
        return (self.__clusterer)

    def get_initial_geography(self):
        '''
        Initial geography for the flow.
        This is set as a method, not a property since it might be expensive to execute.
        It will only be excecuted once in the run() procedure.
        '''
        df = geopandas.read_file(self.shapefile_location)
        df = df.rename(columns={self.id_column: ID})
        return (df)
