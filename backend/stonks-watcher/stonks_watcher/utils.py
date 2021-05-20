from datetime import datetime, timedelta


def older_than(days=0, seconds=0, microseconds=0,
               milliseconds=0, minutes=0, hours=0, weeks=0):
    return (datetime.utcnow() - timedelta(days=days, seconds=seconds, microseconds=microseconds,
                                          milliseconds=milliseconds, minutes=minutes, hours=hours,
                                          weeks=weeks)
            ).isoformat()


def newer_than(days=0, seconds=0, microseconds=0,
               milliseconds=0, minutes=0, hours=0, weeks=0):
    return (datetime.utcnow() - timedelta(days=days, seconds=seconds, microseconds=microseconds,
                                          milliseconds=milliseconds, minutes=minutes, hours=hours,
                                          weeks=weeks)
            ).isoformat()
