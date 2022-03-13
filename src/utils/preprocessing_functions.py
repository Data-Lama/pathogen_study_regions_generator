import numpy as np
import pandas as pd



def one_hot_encoding(df, columns_to_exclude=[]):
    '''
    Method that transforms categorical variables into extra columns where values are 
    encoded in binary form. For each categorical variable, n number of columns will be created
    where n is the number of possible categorical values the given variable can take. (e.g. for the variable sex,
    two extra columns will be created, one for "male" and one for "female", each with a value of 1 or 0.)

    The columns to be transformed are based on the dtypes of the dataframe. 
    Only numerical and datetime dtypes will be automatically excluded, other columns to be excluded 
    should be passed as columns_to_exclude.

    Parameters
    ----------
    df: pandas.DataFrame
        Pandas dataframe to transform

    columns_to_exclude: list (optional)
        List of column names to exclude from encoding

    Returns
    _______
    df: pandas.DataFrame
        Transformed dataframe with one extra column per categorical value

    encoding_dict: dictionary
        Dictionary containing the descriptions of the new columns and how they map back to 
        the original columns
    '''
    # Determine columns of categorical variables
    encoding_dict = {}

    variables_names = df.dtypes.index.to_list()
    categorical_variables = [not (np.issubdtype(i, np.number) or np.issubdtype(i, np.datetime64)) \
        for i in df.dtypes]

    variables_to_encode = []
    for idx, var in enumerate(categorical_variables):
        if var and variables_names[idx] not in columns_to_exclude: variables_to_encode.append(variables_names[idx])

    for var in variables_to_encode:
        translation_dic = {}

        # Assign names to new columns
        new_cols, old_cols = zip(*[(f'{var}_{idx + 1}', i) for idx, i in enumerate(df[var].unique())])
        encoding_dict[var] = dict([(i, j) for i, j in zip(new_cols, old_cols)])
        translation_dic[var] = dict([(j, i) for i, j in zip(new_cols, old_cols)])

        # Create dummy variables
        df_tmp = pd.get_dummies(df[var])
        df_tmp.rename(columns=translation_dic[var], inplace=True)

        # Merge and drop original column 
        df = df.merge(df_tmp, left_index=True, right_index=True)
        df.drop(columns=var, inplace=True)

    return df, encoding_dict
