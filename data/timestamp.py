""" This script converts a UTC date and time to a Unix timestamp."""
from datetime import datetime, timezone

utc_time = datetime(2019, 4, 11, 18, 25, 54, tzinfo=timezone.utc)

unix_timestamp = utc_time.timestamp()

print(f"Unix timestamp: {unix_timestamp}")