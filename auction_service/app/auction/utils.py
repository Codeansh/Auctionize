from datetime import datetime


def convert_datetime(time_str: str,format_str:str):
    try:
        datetime_obj = datetime.strptime(time_str,format_str)
        return datetime_obj,None

    except ValueError as e:
        return None,e

