# Useful date functions
import pandas as pd
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from constants import MONTH, WEEK, YEAR, isTimeResolutionValid


def get_dates_between_years_by_resolution(min_year, max_year, time_resolution):
    '''
    Gets an array of dates corresponding to the given periodicity between the given years (inclusive)
    '''

    start_date = None
    advance_fun = None
    end_date = pd.to_datetime(f"{max_year}-12-31")
    if time_resolution == WEEK:
        start_date = pd.to_datetime(f"{min_year}-01-01")
        # Sets to sunday
        start_date += timedelta(days=6 - start_date.weekday())
        advance_fun = lambda s: s + timedelta(days=7)

    elif time_resolution == MONTH:
        start_date = pd.to_datetime(f"{min_year}-01-31")
        advance_fun = lambda s: s + relativedelta(months=1)

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