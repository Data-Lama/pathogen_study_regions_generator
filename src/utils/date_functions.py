# Useful date functions
from numpy import datetime64
import pandas as pd
from datetime import timedelta

from dateutil.relativedelta import relativedelta

import  constants as con

def get_today():
    return (pd.to_datetime("today"))


def get_dates_between_dates_by_resolution(min_date : datetime64, max_date : datetime64, time_resolution : str):
    '''
    Gets an array of dates corresponding to the given periodicity between the given dates (inclusive)
    '''

    start_date = take_to_resolution_representative(min_date, time_resolution)
    end_date = take_to_resolution_representative(max_date, time_resolution)

    advance_fun = get_resolution_advance_function(time_resolution)
    

    # Builds the responde
    resp = []
    current_date = start_date
    while current_date <= end_date:
        resp.append(current_date)
        current_date = advance_fun(current_date)

    return resp


def get_dates_between_years_by_resolution(min_year : int, max_year : int, time_resolution : str):
    '''
    Gets an array of dates corresponding to the given periodicity between the given years (inclusive)
    '''

    start_date = take_to_resolution_representative(pd.to_datetime(f"{min_year}-01-01"), time_resolution)
    end_date = pd.to_datetime(f"{max_year}-12-31")

    advance_fun = get_resolution_advance_function(time_resolution)
    

    # Builds the responde
    resp = []
    current_date = start_date
    while current_date <= end_date:
        resp.append(current_date)
        current_date = advance_fun(current_date)

    return resp

def compare_time_resolutions(res1, res2):
    '''
    Compares time resolutions.
    if res1 > res2 returns 1.
    if res1 < res2 return -1
    if res1 == res2 return 0
    '''

    # Checks validity
    con.isTimeResolutionValid(res1)
    con.isTimeResolutionValid(res2)

    if res1 == res2:
        return 0

    # Day
    if res1 == con.DAY:
        return 1

    # Week
    if res1 == con.WEEK:
        if res2 == con.DAY:
            return -1

        return 1

    # Month
    if res1 == con.MONTH:
        if res2 == con.YEAR:
            return 1

        return -1
    # Year
    if res1 == con.YEAR:
        return -1

    raise ValueError(f'Time resolution: {res1} not supported')


def take_to_resolution_representative(date, time_resolution):
    '''
    Method that takes the given date and returns the representative, given the time resolution.
    For batch mapping, it is better to use the function: get_period_representative_function
    '''

    fun = get_resolution_representative_function(time_resolution)
    return (fun(date))

def min_inverse_period_representative(date, current_time_resolution, target_time_resolution):
    '''
    Methods that return the min date in the target resolution such that, when taken to the current resolution
    gives the received date. As an example, this method applied to 2000-12-31, with current time resolution: year and
    target resolution day will return 2000-01-01.

    Target resolution should be higher than current resolution
    '''

    # Checks compatibility in resolutions
    con.isTimeResolutionValid(current_time_resolution)
    con.isTimeResolutionValid(target_time_resolution)

    comp = compare_time_resolutions(current_time_resolution, target_time_resolution)

    if comp > 1:
        raise ValueError(f"The target resoltion ({target_time_resolution}) should be higher thant the current resolution ({current_time_resolution})")

    if comp == 0:
        return date

    
    if current_time_resolution == con.YEAR:
        date = pd.to_datetime(f"{date.year}-01-01")
    elif current_time_resolution == con.MONTH:
        date = pd.to_datetime(f"{date.year}-{date.month}-01")
    elif current_time_resolution == con.WEEK:
        date = date - timedelta(days = 6)
    elif current_time_resolution == con.DAY:
        date = date
    else:
        raise ValueError(f"No support for time resolution: {current_time_resolution}")


    return(take_to_resolution_representative(date, target_time_resolution))



def get_resolution_advance_function(time_resolution : str):
    '''
    Gets a function that, given a date in the established time resolution, returs the next date under the same resolution
    '''


    advance_fun = None
    if time_resolution == con.DAY:
        advance_fun = lambda s: s + timedelta(days=1)
    
    elif time_resolution == con.WEEK:
        advance_fun = lambda s: s + timedelta(days=7)

    elif time_resolution == con.MONTH:
        advance_fun = lambda s: (s + relativedelta(days=1) + relativedelta(
            months=1)) - relativedelta(days=1)

    elif time_resolution == con.YEAR:
        advance_fun = lambda s: s + relativedelta(years=1)

    else:
        raise ValueError(f"No support for time resolution: {time_resolution}")

    return(advance_fun)

def get_resolution_representative_function(time_resolution):
    '''
    Method that returns the function that receives a date and takes it to its representative, given the time resolution
    '''

    if time_resolution == con.DAY:
        #Identity
        return(lambda d : d)

    elif time_resolution == con.WEEK:
        # Sets to sunday
        return (lambda d: d + timedelta(days=6 - d.weekday()))

    elif time_resolution == con.MONTH:
        return (lambda d: d.replace(day=1) + relativedelta(months=1) -
                timedelta(days=1))

    elif time_resolution == con.YEAR:
        return (lambda d: d.replace(day=31, month=12))
    else:
        raise ValueError(f"No support for time resolution: {time_resolution}")



def lower_time_resolution(df : pd.DataFrame,
                          initial_time_resolution : str,
                          target_time_resolution : str,
                          aggregation_function : str) -> pd.DataFrame:
    '''
    Method that lowers the time resolution of the given data frame.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to be manipulated. Assumes it has a date and ID columns, the rest are numeric values to be aggregated
    
    initial_time_resolution : string
        Initial time resolution. Check the constants module for available options.
    
    target_time_resolution : string
        Target time resolution. Check the constants module for available options.
    
    aggregation_function : str
        Aggregation funtion to be applied. Available options are MAX, MIN, MEAN and SUM

    Return
    ------
    pd.DataFrame
        DataFrame with the same structure as the parameter DataFrame

    ''' 

    # Checks available aggregation function
    aggregation_function = aggregation_function.lower()
    if aggregation_function not in [con.SUM, con.MIN, con.MAX, con.MEAN]:
        raise ValueError(f"No support for aggregation function: {aggregation_function}")

    # Checks compatibility in resolutions
    con.isTimeResolutionValid(initial_time_resolution)
    con.isTimeResolutionValid(target_time_resolution)

    comp = compare_time_resolutions(initial_time_resolution, target_time_resolution)

    if comp < 0:
        raise ValueError(f"The target resoltion ({target_time_resolution}) should be lower thant the initial resolution ({initial_time_resolution})")

    if comp == 0:
        return df


    # Changes Time resolution
    # -------------------
    # Takes the dates to their corresponding period
    df[con.DATE] = df[con.DATE].apply(
        get_resolution_representative_function(target_time_resolution))
    # Groups by
    df = df.groupby([con.ID, con.DATE]).agg(aggregation_function).reset_index()

    return df
    



def increase_time_resolution(df : pd.DataFrame,
                          initial_time_resolution : str,
                          target_time_resolution : str,
                          extrapolation_function : str) -> pd.DataFrame:
    '''
    Method that increases the time resolution of the given data frame.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to be manipulated. Assumes it has a date and ID columns, the rest are numeric values to be aggregated
    
    initial_time_resolution : string
        Initial time resolution. Check the constants module for available options.
    
    target_time_resolution : string
        Target time resolution. Check the constants module for available options.
    
    extrapolation_function : str
        Aggregation funtion to be used to extrapolate between dates. Available options are PAD and LINEAR

    Return
    ------
    pd.DataFrame
        DataFrame with the same structure as the parameter DataFrame

    ''' 

    # Checks available aggregation function
    extrapolation_function = extrapolation_function.lower()
    if extrapolation_function not in [con.LINEAR, con.PAD]:
        raise ValueError(f"No support for extrapolation function: {extrapolation_function}")

    # Checks compatibility in resolutions
    con.isTimeResolutionValid(initial_time_resolution)
    con.isTimeResolutionValid(target_time_resolution)

    comp = compare_time_resolutions(initial_time_resolution, target_time_resolution)

    if comp > 0:
        raise ValueError(f"The target resoltion ({target_time_resolution}) should be higher thant the initial resolution ({initial_time_resolution})")

    if comp == 0:
        return df


    # Changes Time resolution
    # -------------------
    # Constructs all dates

    # Adjusts dates in dataframe
    df[con.DATE] = df[con.DATE].apply(get_resolution_representative_function(target_time_resolution))
    
    start_date =  df[con.DATE].min()
    end_date = df[con.DATE].max()


    all_dates = get_dates_between_dates_by_resolution(
        min_date = start_date,
        max_date = end_date,
        time_resolution=target_time_resolution)
    
    # Creates merging column
    df_all_dates = pd.DataFrame({con.DATE: all_dates})
    df_all_ids = pd.DataFrame({con.ID : df[con.ID].unique()})

    df_all = df_all_ids.merge(df_all_dates, how = 'cross')

    # Merges
    df = df_all.merge(df, how='left')

    # Extract value columns
    value_cols = df.columns.difference([con.ID, con.DATE]).values.tolist()

    # Group and interpolates
    def grouped_interpolate(df):

        df = df.sort_values(con.DATE)
        df[value_cols] = df[value_cols].interpolate(method = extrapolation_function)

        return(df)

    df = df.groupby(con.ID).apply(grouped_interpolate).reset_index(drop = True)

    # Orders columns
    return (df[[con.ID, con.DATE] +
                   df.columns.difference([con.ID, con.DATE]).values.tolist()].copy())




