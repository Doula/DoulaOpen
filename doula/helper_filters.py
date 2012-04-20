import datetime

def get_status_class(status):
    return get_class('status', status)

def get_stat_class(status):
    return get_class('stat', status)

def get_class(prefix, status):
    if status == 'unchanged':
        return prefix + '-unchanged'
    elif status == 'uncommitted_changes':
        return prefix + '-error'
    elif status == 'unknown':
        return prefix + '-unknown'
    else:
        return prefix + '-changed'

def format_datetime(date):
    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:8])
    hour = int(date[8:10])
    minute = int(date[10:12])
    second = int(date[12:14])

    d = datetime.datetime(year, month, day, hour, minute, second)
    format = '%m/%d/%Y %I:%M %p'
    return d.strftime(format)