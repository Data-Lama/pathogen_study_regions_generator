# Test Flow

from clusterers.specific.identity_clusterer import IdentityClusterer
from constants import WEEK
from embedders.specific.identity_embedder import IdentityEmbbeder
from flows.abstract.abstract_flow import AbstractFlow

import geopandas


class TestFlow(AbstractFlow):

    def __init__(self,
                 ID,
                 name,
                 time_resolution,
                 shapefile_location,
                 vector_data_sources=[],
                 matrix_data_sources=[],
                 embedder=IdentityEmbbeder,
                 clusterer=IdentityClusterer):
        super().__init__()

        self.ID = ID
        self.name = name
        self.time_resolution = time_resolution
        self.vector_data_sources = vector_data_sources
        self.matrix_data_sources = matrix_data_sources
        self.embedder = embedder
        self.clusterer = clusterer
        self.shapefile_location = shapefile_location

    def get_initial_geography(self):
        '''
        Initial geography for the flow.
        This is set as a method, not a property since it might be expensive to execute.
        It will only be excecuted once in the run() procedure.
        '''

        return (geopandas.read_file(self.shapefile_location))
