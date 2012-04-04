
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