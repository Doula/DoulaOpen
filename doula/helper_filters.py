
def get_status_class(status):
    if status == 'unchanged':
        return 'status-unchanged'
    elif status == 'uncommitted_changes':
        return 'status-error'
    else:
        return 'status-changed'


def get_stat_class(status):
    if status == 'unchanged':
        return 'stat-unchanged'
    elif status == 'uncommitted_changes':
        return 'stat-error'
    else:
        return 'stat-changed'