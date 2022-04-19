# Different functions for publication purposes

column_name_dic = {}
column_name_dic['coca_coca_total'] = "Coca"
column_name_dic['gold_stock_price_value'] = "Gold Stock Price"
column_name_dic[
    'precipitation_total_precipitation_average'] = "Total Precipitation"
column_name_dic['temperature_mean_temperature_average'] = "Average Temperature"
column_name_dic[
    'average_deforestation_deforestation_average'] = "Average Deforestation"
column_name_dic[
    'precipitation_average_precipitation_average'] = "Average Precipitation"


def beautify_data_column_name(col_name):
    """
    Method that given a data column name, returns a human readeble text
    """

    if col_name in column_name_dic:
        return (column_name_dic[col_name])

    return (col_name)
