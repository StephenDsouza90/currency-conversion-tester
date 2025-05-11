from unittest.mock import patch, MagicMock

from src.currency_utils import get_currency_rate


@patch("src.currency_utils.CountryInfo")
@patch("src.currency_utils.CurrencyConverter")
def test_get_currency_rate_true(mock_currency_converter, mock_country_info):
    """
    Test the get_currency_rate function to check if the currency rate is above the threshold.
    """
    mock_country_info.return_value.run.return_value = ("GBP", None)
    mock_currency_converter.return_value.convert_currency.return_value = (1.23, None)
    mock_driver = MagicMock()

    rate, currency, error = get_currency_rate(mock_driver, "GB")
    assert rate == 1.23
    assert currency == "GBP"
    assert error is None


@patch("src.currency_utils.CountryInfo")
@patch("src.currency_utils.CurrencyConverter")
def test_get_currency_rate_false(mock_currency_converter, mock_country_info):
    """
    Test the get_currency_rate function to check if the currency rate is below the threshold.
    """
    mock_country_info.return_value.run.return_value = ("TRY", None)
    mock_currency_converter.return_value.convert_currency.return_value = (0.23, None)
    mock_driver = MagicMock()

    rate, currency, error = get_currency_rate(mock_driver, "TR")
    assert rate == 0.23
    assert currency == "TRY"
    assert error is None
