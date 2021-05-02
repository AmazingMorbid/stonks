from datetime import datetime, timedelta

import pytz


def older_than_datetime_iso(_timedelta: timedelta):
    return (datetime.now(pytz.utc) - _timedelta).isoformat()
