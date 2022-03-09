# Identity Embedder (does not alter the received inputs)

from embedders.abstract.embedder import AbstractEmbbeder


class IdentityEmbbeder(AbstractEmbbeder):

    ID = "identity_embedder"
    name = "Identity Embedder"

    def embeddVector(self, df_vector=None, df_matrix=None):
        '''
        Returns the input as it is given
        '''

        return (df_vector, df_matrix)
