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
