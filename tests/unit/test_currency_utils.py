from unittest.mock import patch, MagicMock

from src.currency_utils import get_currency_rate, check_threshold


@patch("src.currency_utils.CountryInfo")
@patch("src.currency_utils.CurrencyConverter")
def test_get_currency_rate_success(
    mock_currency_converter, mock_country_info
):
    """
    Test the get_currency_rate function for successful currency retrieval.
    """
    mock_country_info.return_value.run.return_value = ("GBP", None)
    mock_currency_converter.return_value.convert_currency.return_value = (1.2, None)
    mock_driver = MagicMock()

    rate, currency, error = get_currency_rate(mock_driver, "GB")
    assert rate == 1.2
    assert currency == "GBP"
    assert error is None


@patch("src.currency_utils.CountryInfo")
def test_get_currency_rate_country_info_error(mock_country_info):
    """
    Test the get_currency_rate function for error in CountryInfo.
    """
    mock_country_info.return_value.run.return_value = (None, "CountryInfo error")
    mock_driver = MagicMock()

    rate, currency, error = get_currency_rate(mock_driver, "ZZ")
    assert rate is None
    assert currency is None
    assert error == "CountryInfo error"


@patch("src.currency_utils.CountryInfo")
@patch("src.currency_utils.CurrencyConverter")
def test_get_currency_rate_currency_converter_error(
    mock_currency_converter, mock_country_info
):
    """
    Test the get_currency_rate function for error in CurrencyConverter.
    """
    mock_country_info.return_value.run.return_value = ("GBP", None)
    mock_currency_converter.return_value.convert_currency.return_value = (
        None,
        "CurrencyConverter error",
    )
    mock_driver = MagicMock()

    rate, currency, error = get_currency_rate(mock_driver, "ZZ")
    assert rate is None
    assert currency == "GBP"
    assert error == "CurrencyConverter error"


def test_check_threshold_above():
    """
    Test the check_threshold function for rate above threshold.
    """
    assert check_threshold(1.5, 1) is True


def test_check_threshold_below():
    """
    Test the check_threshold function for rate below threshold.
    """
    assert check_threshold(0.5, 1) is False
