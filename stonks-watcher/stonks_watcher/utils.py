from datetime import datetime, timedelta


def older_than(_timedelta: timedelta):
    return (datetime.utcnow() - _timedelta).isoformat()
