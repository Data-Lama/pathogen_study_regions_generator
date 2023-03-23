# Geography from a flow output
from constants import CLUSTER_ID, ID, SUB_ID
from geography.abstract.abstact_geography import Geography


class GeographyFromFlowOutput(Geography):

    def __init__(self, id, name, flow):
        '''
        Builds a geography from a geopandas dataframe

        Parameters
        ----------
        id : string
            Id of the geography
        name : string
            Name of the geography
        flow : Flow
            Excecuted flow

        '''

        super().__init__()
        self.__id = id
        self.__name = name
        self.__geometry = flow.final_geometry
        self.sub_geography = flow.geography
        self.df_map = flow.clustered_ids.rename(columns={
            ID: SUB_ID,
            CLUSTER_ID: ID
        })

    @property
    def ID(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    def build_geometry(self):
        return (self.__geometry)
