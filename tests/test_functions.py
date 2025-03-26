import t8_client.functions as fun


def test_unix_timestamp_conversion() -> None:
    # Case 1: Convert ISO string of January 1st, 1970 to Unix timestamp
    iso_time_str = "1970-01-01T00:00:00"
    expected_ts = 0  # Unix epoch time
    assert fun.get_unix_timestamp_from_iso(iso_time_str) == expected_ts

    # Case 2: Convert specific ISO string to Unix timestamp
    iso_time_str = "2025-03-25T13:56:23"  # March 25, 2025, 13:56:23 UTC
    expected_ts = 1742910983
    assert fun.get_unix_timestamp_from_iso(iso_time_str) == expected_ts

    # Case 3: Convert ISO string from before 1970 (negative timestamp)
    iso_time_str = "1969-12-31T23:00:00"  # December 31, 1969, 23:00:00 UTC
    expected_ts = -3600
    assert fun.get_unix_timestamp_from_iso(iso_time_str) == expected_ts


def test_get_iso_from_unix_timestamp() -> None:
    # Case 1: Timestamp for January 1st, 1970
    timestamp = 0
    expected_result = "1970-01-01T00:00:00"
    assert fun.get_iso_from_unix_timestamp(timestamp) == expected_result

    # Case 2: Specific date timestamp
    timestamp = 1633089600  # October 1st, 2021, 12:00:00 UTC
    expected_result = "2021-10-01T12:00:00"
    assert fun.get_iso_from_unix_timestamp(timestamp) == expected_result

    # Case 3: Negative timestamp (before 1970)
    timestamp = -3600  # December 31, 1969 23:00:00 UTC
    expected_result = "1969-12-31T23:00:00"
    assert fun.get_iso_from_unix_timestamp(timestamp) == expected_result
