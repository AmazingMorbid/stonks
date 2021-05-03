from datetime import datetime, timedelta

import pytz


def older_than_datetime_iso(_timedelta: timedelta):
    return (datetime.utcnow() - _timedelta).isoformat()
