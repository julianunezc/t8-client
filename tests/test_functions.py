import pytest
from pytest_mock import MockerFixture

import t8_client.functions as fun


def test_fetch_data_success(mocker: MockerFixture) -> None:
    """
    Test to simulate a successful API response.
    """
    # We will simulate the response we expect from the API
    mock_response = mocker.MagicMock()
    mock_response.status_code = (
        200  # Simulate a successful response with status code 200
    )
    mock_response.json.return_value = {
        "key": "value"
    }  # Simulate the JSON response from the API

    # Simulate that requests.get returns the mock_response
    mocker.patch("requests.get", return_value=mock_response)

    # Now we call the function we want to test
    url = "https://api.example.com/data"
    user = "test_user"
    passw = "test_pass"

    # Call the fetch_data function with the mocked data
    result = fun.fetch_data(url, user, passw)

    # Check that the function returns the correct simulated response
    assert result == {"key": "value"}


def test_fetch_data_error(mocker: MockerFixture) -> None:
    """
    Test to simulate an error response (status code 500).
    """
    # We will simulate a response with an error status code (500)
    mock_response = mocker.MagicMock()
    mock_response.status_code = 500  # Simulate an error response with status code 500
    mock_response.json.return_value = {
        "error": "Server error"
    }  # Simulate the error message

    # Simulate that requests.get returns the mock_response
    mocker.patch("requests.get", return_value=mock_response)

    # We expect the function to terminate the program due to the 500 status code
    url = "https://api.example.com/data"
    user = "test_user"
    passw = "test_pass"

    # Check if SystemExit is raised (this will stop the program)
    with pytest.raises(SystemExit):
        fun.fetch_data(url, user, passw)


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
