# Agreggation Embedder (does not alter the received inputs)

from embedders.abstract.embedder import AbstractEmbbeder
import constants as con

class AggregationEmbedder(AbstractEmbbeder):

    ID = "aggregation_embedder"
    name = "Aggregation Embedder"

    def embeddData(self, df_vector=None, df_matrix=None, aggregation_function='sum'):
        '''
        Aggregate based on provided function. Default behavior is sum
        '''

        df_vector = df_vector.groupby(con.ID).apply(aggregation_function).reset_index()

        return (df_vector, None)
