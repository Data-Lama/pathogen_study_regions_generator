# Geographic functions
import geopandas
import numpy as np
import pandas as pd

from constants import AREA_COL, DATE, AVERAGE, GEOMETRY, ID, ID_1, ID_2, MANIPULATION_PROJECTION, MAX, MIN, SUB_ID, SUM, TOTAL, get_grouping, make_grouping_name


# Constructs function for overlay
def __construct_agglomeration_function(included_groupings=[]):
    '''
    Function that constructs the agglomeration function. If included groupings
    is not empty, the corresponding groupings will be formed for each value column. If 
    not, the agglomeration function will be infered from the end text of the colum
    '''

    def extract_values(df):

        final_cols = []
        for col in df.columns:
            if col in [ID, GEOMETRY, DATE]:
                continue
            final_cols += [f"{col}_{gr}" for gr in included_groupings]

        # Computes ares
        area = df.geometry.to_crs(MANIPULATION_PROJECTION).area.sum()

        response = {}
        for col in final_cols:
            if col in [ID, GEOMETRY, DATE]:
                continue
            if col.endswith(f"_{MAX}"):
                response[col] = df[col].max()
            elif col.endswith(f"_{MIN}"):
                response[col] = df[col].min()
            elif col.endswith(f"_{SUM}"):
                response[col] = df[col].sum()
            elif col.endswith(f"_{TOTAL}"):
                response[col] = (
                    df[col] *
                    df.geometry.to_crs(MANIPULATION_PROJECTION).area).sum()
            elif col.endswith(f"_{AVERAGE}"):
                response[col] = (df[col] * df.geometry.to_crs(
                    MANIPULATION_PROJECTION).area).sum() / area
            else:
                raise ValueError(
                    "Cannot group column: {col}, groupping no implemented")

        return (pd.DataFrame([response]))

    return (extract_values)


def agglomerate_data_frame(df: pd.DataFrame,
                           grouping_columns: list,
                           included_groupings=[]):
    '''
    Method that agglomerates a given dataframe by their grouping columns.
    It uses the included groupings to infer the agglomerations. If this parameter
    is empty, the agglomertion scheme is infered from the column's ending.

    Parameters
    ----------
    df : Pandas or Geopandas dataframe.
        The values to agglomerate. If TOTAL or AVERAGE are included in the groupings or in
        the current columns, must be a Geopandas element to construct to infer the area.
         Geopandas dataframe with the geometry to be overlayed. Will only use the columns ID and geometry
    grouping_columns : array
        Columns that must be grouped over. If empty, the grouping will be infered from the column's name ending.
    included_groupings : array
        Grouping functions to be applied. The available are:
            - MAX: Maximum of the values of all intersecting polygons
            - MIN: Minimum of the values of all intersecting polygons
            - SUM: The sum of the values of all intersecting polygons
            - TOTAL: The sum of the values multiplied by the area of each intersecting polygon
            - AVERAGE: The sum of the values multiplied by the area of each intersecting polygon divided by the total sum of the intersecting polygons.



    Return
    ------
    pandas.DataFrame
        Agglomerated DataFrame
    '''

    # Extracts the value columns
    value_cols = df.columns.difference(
        [DATE, GEOMETRY, ID, ID_1, ID_2, SUB_ID, AREA_COL])

    # Creates the columns for aggregations
    for col in value_cols: 
        for gr in included_groupings:                   
            df[make_grouping_name(col, gr)] = df[col]

        if len(included_groupings) > 0:
            # Drops original column (if gropuings where found)
            df = df.drop(col, axis=1)

    # Refreshes value columns
    value_cols = df.columns.difference(
        [DATE, GEOMETRY, ID, ID_1, ID_2, SUB_ID, AREA_COL])
    final_groupings = np.unique([get_grouping(col) for col in value_cols])

    # Checks if area needs to be computed    
    if TOTAL in final_groupings or AVERAGE in final_groupings:
        if GEOMETRY not in df.columns and AREA_COL not in df.columns:
            raise ValueError(
                "Dataframe must include geometry or polygon_area if TOTAL or AVERAGE agglomerations are included."
            )

        if AREA_COL not in df.columns:
            df[AREA_COL] = df[GEOMETRY].to_crs(MANIPULATION_PROJECTION).area

    if AREA_COL not in df.columns:
        df[AREA_COL] = 0  # Compatibility

    # Builds agg dictionary
    fun_dic = {AREA_COL: SUM}
    for col in value_cols:
        gr = get_grouping(col)
        if gr in [AVERAGE, TOTAL]:
            df[col] = df[col] * df[AREA_COL]
            fun_dic[col] = SUM
        else:
            fun_dic[col] = gr

    # Aggregates

    df_agg = df.groupby(grouping_columns).agg(fun_dic).reset_index()

    # Corrects AVERAGE columns
    for col in value_cols:
        if get_grouping(col) == AVERAGE:
            df_agg[col] = df_agg[col] / df_agg[AREA_COL]

    # Drops Area column
    df_agg.drop(AREA_COL, axis=1, inplace=True)

    return (df_agg)


def overlay_over_geo(df_values: geopandas.GeoDataFrame,
                     df_geo: geopandas.GeoDataFrame,
                     grouping_columns=[ID, DATE],
                     included_groupings=[SUM, TOTAL, AVERAGE, MAX, MIN],
                     default_values=np.nan):
    '''
    Method that overlays the given df over the geographic dataframe

    Parameters
    ----------
    df_values : Geopandas.DataFrame
        Geopandas dataframe with the values to overlay. This method assumes that anything other than
        than the grouping columns and geometry is a value that must be overlayed.
    df_geo : Geopandas.DataFrame
        Geopandas dataframe with the geometry to be overlayed. Will only use the columns ID and geometry
    grouping_columns : array
        Columns that must be grouped over
    included_groupings : array
        Grouping functions to be applied 
    default_values : value or dict
        Value or dict indicating the default values for geometries where no value could be extracted
    '''

    df_geo = df_geo[[ID, GEOMETRY]].copy()

    df_overlayed = geopandas.overlay(df_geo,
                                     df_values,
                                     how='intersection',
                                     keep_geom_type=True)

    # Aggregates
    df_overlayed = agglomerate_data_frame(df_overlayed, grouping_columns,
                                          included_groupings)

    # Fills Nas
    if DATE in grouping_columns:
        # Adds default by date
        # Builds total DF
        geo_ids = df_geo[ID].unique()
        dfs = []
        for date in df_values[DATE].unique():
            dfs.append(pd.DataFrame({ID: geo_ids, DATE: date}))

        df_global = pd.concat(dfs, ignore_index=True)
        df_overlayed = df_global.merge(df_overlayed, how='left')

    else:
        df_overlayed = df_geo[[ID]].merge(df_overlayed, how='left')

    if default_values is not None:
        if type(default_values) is dict and len(included_groupings) > 0:
            new_default_values = {}
            for gr in included_groupings:
                for col in default_values:
                    new_default_values[make_grouping_name(
                        col, gr)] = default_values[col]

            default_values = new_default_values

        df_overlayed = df_overlayed.fillna(default_values)

    return (df_overlayed)


def get_enclosing_geoemtry(df_geo):
    '''
    Gets the enclosing geometry as a geopandas from the given
    geopandas
    '''
    return (df_geo[[GEOMETRY]].dissolve())
