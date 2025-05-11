import requests
import json

from src.country_info import CountryInfo


def test_extract_currency_with_valid_country_code():
    """
    Test the extract_currency function with a valid country code.
    """
    mock_response = [{"currencies": {"GBP": {}}}]

    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps(mock_response).encode("utf-8")

    currency, error = CountryInfo().extract_currency(response)

    assert currency == "GBP"
    assert error is None


def test_extract_currency_with_missing_currencies_key():
    """
    Test the extract_currency function with a response missing the currencies key.
    """
    mock_response = [{"name": "United Kingdom"}]

    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps(mock_response).encode("utf-8")

    currency, error = CountryInfo().extract_currency(response)

    assert currency is None
    assert error is not None
    assert str(error) == "Error: No currency data found."


def test_extract_currency_with_no_data():
    """
    Test the extract_currency function with a response that has no data.
    """
    mock_response = []

    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps(mock_response).encode("utf-8")

    currency, error = CountryInfo().extract_currency(response)

    assert currency is None
    assert error is not None
    assert str(error) == "Error: Invalid response format."


def test_extract_currency_with_invalid_country_code():
    """
    Test the extract_currency function with an invalid country code.
    """
    mock_response = {"message": "Country not found"}

    response = requests.Response()
    response.status_code = 404
    response._content = json.dumps(mock_response).encode("utf-8")

    currency, error = CountryInfo().extract_currency(response)

    assert currency is None
    assert error is not None
    assert str(error) == "Error: Country not found"


def test_extract_currency_with_multiple_currencies():
    """
    Test the extract_currency function with a response containing multiple currencies.
    """
    mock_response = [{"currencies": {"USD": {}, "EUR": {}}}]

    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps(mock_response).encode("utf-8")

    currency, error = CountryInfo().extract_currency(response)

    assert currency == "USD"
    assert error is None


def test_extract_currency_with_empty_currencies():
    """
    Test the extract_currency function with a response having an empty currencies dictionary.
    """
    mock_response = [{"currencies": {}}]

    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps(mock_response).encode("utf-8")

    currency, error = CountryInfo().extract_currency(response)

    assert currency is None
    assert error is not None
    assert str(error) == "Error: No currency data found."


def test_extract_currency_with_malformed_currency_code():
    """
    Test the extract_currency function with a malformed currency code.
    """
    mock_response = [{"currencies": {"INVALID": {}}}]

    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps(mock_response).encode("utf-8")

    currency, error = CountryInfo().extract_currency(response)

    assert currency is None
    assert error is not None
    assert str(error) == "Error: Invalid currency code format."


def test_extract_currency_with_non_200_status_and_no_error_message():
    """
    Test the extract_currency function with a non-200 status code and no error message.
    """
    response = requests.Response()
    response.status_code = 404
    response._content = b""

    currency, error = CountryInfo().extract_currency(response)

    assert currency is None
    assert error is not None
    assert str(error) == "Error: Invalid response format."


def test_extract_currency_with_unexpected_data_types():
    """
    Test the extract_currency function with unexpected data types in the response.
    """
    mock_response = [{"currencies": ["USD", "EUR"]}]

    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps(mock_response).encode("utf-8")

    currency, error = CountryInfo().extract_currency(response)

    assert currency is None
    assert error is not None
    assert str(error) == "Error: API response format changed."


def test_extract_currency_with_empty_response_body():
    """
    Test the extract_currency function with a valid status code but an empty response body.
    """
    response = requests.Response()
    response.status_code = 200
    response._content = b""

    currency, error = CountryInfo().extract_currency(response)

    assert currency is None
    assert error is not None
    assert str(error) == "Error: Invalid response format."
