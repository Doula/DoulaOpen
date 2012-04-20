import datetime

def get_status_class(status):
    return get_class('status', status)

def get_stat_class(status):
    return get_class('stat', status)

def get_class(prefix, status):
    if status == 'deployed':
        return prefix + '-deployed'
    elif status == 'tagged':
        return prefix + '-tagged'
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

def get_pretty_status(status):
    """
    Return a print friendly status
    """
    statuses = {
        'tagged': 'Tagged',
        'deployed': 'Deployed',
        'change_to_config': 'Changes to Configuration',
        'change_to_app': 'Changes to Application Environment',
        'change_to_app_and_config': 'Changes to Configuration and Application Environment',
        'uncommitted_changes': 'Uncommitted Changes'
    }
    
    if status in statuses:
        return statuses[status]
    else:
        return 'Unknown'