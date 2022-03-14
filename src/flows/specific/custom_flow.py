# Test Flow

from clusterers.specific.identity_clusterer import IdentityClusterer
from embedders.specific.identity_embedder import IdentityEmbbeder
from flows.abstract.abstract_flow import AbstractFlow


class CustomFlow(AbstractFlow):

    def __init__(self,
                 ID,
                 name,
                 time_resolution,
                 geography,
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
        self.__geography = geography

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

    @property
    def geography(self):
        return (self.__geography)
