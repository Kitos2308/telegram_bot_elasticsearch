import pandas as pd

import datetime as dt

from analytic.analytic import Analytic


def read_file(path):
    def convert_datetime(val):
        try:
            return dt.datetime.strptime(val, "%Y-%m-%d %H:%M:%S,%f")
        except ValueError:
            return

    def read_str(value):
        length = len(value)
        return value[0:int(length - 2)]


    df = pd.read_csv(path, encoding='utf-8', sep=": ", engine='python',
                     names=["date", "level", "ip_address", "sid", "method", "api_route", "phone", "mistake"],
                     usecols=["date", "level", "ip_address", "sid", "method", "api_route", "phone", "mistake"],
                     converters={'date': convert_datetime, 'mistake':read_str}, index_col=False,
                     na_values=["<CIMultiDictProxy('Server'", "Traceback (most recent call last):"],

                     skip_blank_lines=True)
    return df


def get_mask(frame, level):

    mask_level = frame["level"]  # sort by method

    mask_level_ = frame.loc[mask_level == level]  # assign all stream with LEVEL from function as parameter
    return mask_level_

def last_time(frame):
    if frame.empty:
        return None
    else:
        time=frame.iloc[-1, 0]
        return time

def time_before_last(frame):
    if frame.empty:
        return None
    else:
        time=frame.iloc[-2, 0]
        return time

def mask_time(frame, time):
    date_frame=frame['date']
    mask=date_frame>time
    frame_=frame.loc[mask,:]
    return frame_


