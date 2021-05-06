from datetime import datetime, timedelta

import pytz


def older_than(_timedelta: timedelta):
    return (datetime.utcnow() - _timedelta).isoformat()
