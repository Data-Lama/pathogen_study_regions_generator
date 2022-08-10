# Useful date functions
import pandas as pd
from datetime import timedelta

from dateutil.relativedelta import relativedelta

from constants import DAY, MONTH, WEEK, YEAR, isTimeResolutionValid


def get_today():
    return (pd.to_datetime("today"))


def get_dates_between_years_by_resolution(min_year, max_year, time_resolution):
    '''
    Gets an array of dates corresponding to the given periodicity between the given years (inclusive)
    '''

    start_date = None
    advance_fun = None
    end_date = pd.to_datetime(f"{max_year}-12-31")
    if time_resolution == DAY:
        start_date = pd.to_datetime(f"{min_year}-01-01")
        advance_fun = lambda s: s + timedelta(days=1)
    
    elif time_resolution == WEEK:
        start_date = pd.to_datetime(f"{min_year}-01-01")
        # Sets to sunday
        start_date += timedelta(days=6 - start_date.weekday())
        advance_fun = lambda s: s + timedelta(days=7)

    elif time_resolution == MONTH:
        start_date = pd.to_datetime(f"{min_year}-01-31")
        advance_fun = lambda s: (s + relativedelta(days=1) + relativedelta(
            months=1)) - relativedelta(days=1)

    elif time_resolution == YEAR:
        start_date = pd.to_datetime(f"{min_year}-12-31")
        advance_fun = lambda s: s + relativedelta(years=1)

    else:
        raise ValueError(f"No support for time resolution: {time_resolution}")

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
    isTimeResolutionValid(res1)
    isTimeResolutionValid(res2)

    if res1 == res2:
        return 0

    # Day
    if res1 == DAY:
        return -1

    # Week
    if res1 == WEEK:
        if res2 == DAY:
            return 1

        return -1

    # Month
    if res1 == MONTH:
        if res2 == YEAR:
            return -1

        return 1
    # Year
    if res1 == YEAR:
        return 1

    raise ValueError(f'Time resolution: {res1} not supported')


def take_to_period_representative(date, time_resolution):
    '''
    Method that takes the given date and returns the representative, given the time resolution.
    For batch mapping, it is better to use the function: get_period_representative_function
    '''

    fun = get_period_representative_function(time_resolution)
    return (fun(date))


def get_period_representative_function(time_resolution):
    '''
    Method that returns the function that receives a date and takes it to its representative, given the time resolution
    '''

    if time_resolution == DAY:
        #Identity
        return(lambda d : d)

    elif time_resolution == WEEK:
        # Sets to sunday
        return (lambda d: d + timedelta(days=6 - d.weekday()))

    elif time_resolution == MONTH:
        return (lambda d: d.replace(day=1) + relativedelta(months=1) -
                timedelta(days=1))

    elif time_resolution == YEAR:
        return (lambda d: d.replace(day=31, month=12))
    else:
        raise ValueError(f"No support for time resolution: {time_resolution}")
