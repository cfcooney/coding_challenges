from datetime import datetime, timezone

def safe_timestamp(dt: datetime) -> float:
    # If naive, assume it's UTC (change to your truth if needed)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    return (dt - epoch).total_seconds()