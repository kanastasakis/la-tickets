class DateCount(object):
    def __init__(self, **kwargs):
        for field in ('date', 'count'):
            setattr(self, field, kwargs.get(field, None))

class DayStats(object):
    def __init__(self, **kwargs):
        for field in ('day', 'avg', 'std'):
            setattr(self, field, kwargs.get(field, None))

class MonthStats(object):
    def __init__(self, **kwargs):
        for field in ('month', 'avg', 'std'):
            setattr(self, field, kwargs.get(field, None))