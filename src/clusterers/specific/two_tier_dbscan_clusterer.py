# Two tier DBSCAN
import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances
from clusterers.abstract.clusterer import AbstractClusterer
import constants as con

from sklearn.cluster import DBSCAN

DEFAULT_EPS = lambda x: np.percentile(x, 0.25)

id = "two_tier_dbscan_clusterer"
name = "Two Tier DBSCAN Clusterer"


class TwoTierDBSCANClusterer(AbstractClusterer):
    '''
    Implementation of a two tier DBSCAN algorithm. The idea of this clustering method is to preform 
    the ususal Density-based spatial clustering of applications with noise but over two different distance matrices.
    The first matrix will be computed using a single column from the embedded matrix and the second will be computed as the
    given distance between the embedded vectors.

    This implementation uses the sklearn DBSCAN class
    '''

    def __init__(self,
                 matrix_col,
                 metric,
                 eps_1=DEFAULT_EPS,
                 eps_2=DEFAULT_EPS):
        '''
        Parameters
        ----------
        matrix_col : string
            The column from the matrix dataframe that will be used.
        metric : string
            Metric string to construct the attribute distance matrix
        eps_1 : float or function
            First epsylon value to be use to define neighbors over the first matrix. If a function, it will be excecuted 
            with the distance matrix as input. Default value is to select the 25% percentile of the distances.
        eps_2 : float or function
            First epsylon value to be use to define neighbors over the second matrix. If a function, it will be excecuted 
            with the distance matrix as input. This parameter is passed directly to the DBSCAN class. Default value is to select the 25% 
            percentile of the distances.
        '''
        super().__init__()

        # The column to use as a distance from the matrix dataframe
        self.matrix_col = matrix_col

        # The sklearn metric
        self.metric = metric

        # eps
        self.eps_1 = eps_1
        self.eps_2 = eps_2

    @property
    def ID(self):
        return id

    @property
    def name(self):
        return name

    def clusterData(self, current_geography, df_vector=None, df_matrix=None):

        # Uses the df_matrix for the first distance and computes the other distance matrix from
        # the vector data

        if df_vector is None and df_matrix is None:
            raise ValueError(
                "Error in cluster. Neither df_vector or df_matrix can be None")

        # Extracts the ids
        ids = list(
            set(df_vector[con.ID].unique()).intersection(
                df_matrix[con.ID_1].unique()).intersection(
                    df_matrix[con.ID_2].unique()))

        # Makes the first distance matrix (distance)
        df_distance_matrix = df_matrix.pivot(index=con.ID_1,
                                             columns=con.ID_2,
                                             values=self.matrix_col)

        distance_matrix = df_distance_matrix.loc[ids, ids].values

        # Fills diagonal
        np.fill_diagonal(distance_matrix, 0)

        # Makes the second distance matrix (attribute matrix)
        df_vector = df_vector.set_index(con.ID).loc[ids]
        attribute_matrix = pairwise_distances(df_vector, metric=self.metric)

        # Computes eps_1
        eps_1_numeric = self.eps_1
        if callable(self.eps_1):
            eps_1_numeric = self.eps_1(distance_matrix)

        # Computes eps_2
        eps_2_numeric = self.eps_2
        if callable(self.eps_2):
            eps_2_numeric = self.eps_2(attribute_matrix)

        # Filters first matrix
        distance_matrix[distance_matrix > eps_1_numeric] = np.inf
        distance_matrix[distance_matrix <= eps_1_numeric] = 1

        # Computes max
        attr_max = attribute_matrix.max()
        # Defines the final distance matrix
        # For this implemenatation 0*inf = inf
        attribute_matrix[np.logical_and(distance_matrix == np.inf,
                                        attribute_matrix == 0)] = np.inf

        final_distance_matrix = distance_matrix * attribute_matrix

        # Sets np.inf = 100*eps
        final_distance_matrix[final_distance_matrix == np.inf] = max(
            eps_2_numeric, attr_max) * 10e5

        # Debug
        #self.distance_matrix = distance_matrix
        #self.attribute_matrix = attribute_matrix
        #self.final_distance_matrix = final_distance_matrix

        # Preforms DBSCAN
        self.clustering = DBSCAN(
            eps=eps_2_numeric, min_samples=1,
            metric="precomputed").fit(final_distance_matrix)

        # Builds return object
        results = pd.DataFrame({
            con.ID: ids,
            con.CLUSTER_ID: self.clustering.labels_
        })

        return (results)
