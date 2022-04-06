# Community detection over similarity
from clusterers.abstract.clusterer import AbstractClusterer
import constants as con
import pandas as pd

import networkx as nx
from networkx.algorithms.community import asyn_lpa_communities

id = "similarity_community_clusterer"
name = "Similarity Community Clusterer"


class SimilarityCommunityClusterer(AbstractClusterer):
    '''
    Implementation of label propagation communities over a similarity network, like a mobility network
    '''

    def __init__(self, similarity_col):
        '''
        Parameters
        ----------
        similarity_col : string
            The column from the matrix dataframe that will be used as weights for the graph.
        '''
        super().__init__()

        # The column to use as a distance from the matrix dataframe
        self.similarity_col = similarity_col

    @property
    def ID(self):
        return id

    @property
    def name(self):
        return name

    def clusterData(self, current_geography, df_vector=None, df_matrix=None):

        # Extracts Ids
        ids = current_geography.get_geometry()[con.ID].values

        # Builds return object
        results = pd.DataFrame({con.ID: ids, con.CLUSTER_ID: None})

        # Builds Graph
        # Skips self loops
        G = nx.DiGraph()
        for _, row in df_matrix.iterrows():
            if row[con.ID_1] != row[con.ID_2]:
                G.add_edge(row[con.ID_1],
                           row[con.ID_2],
                           weight=row[self.similarity_col])

        # Excecutes algorithm
        res = asyn_lpa_communities(G, weight='weight')

        # Assigns Cluster
        i = 0
        for r in res:
            results.loc[results[con.ID].isin(r), con.CLUSTER_ID] = i
            i += 1

        return (results)
