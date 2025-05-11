from unittest.mock import MagicMock, patch

import pytest
from selenium.webdriver.common.keys import Keys

from src.currency_converter import CurrencyConverter
from src.error import Error


@pytest.fixture
def mock_driver():
    with patch("src.currency_converter.webdriver.Chrome") as MockWebDriver:
        yield MockWebDriver()


@pytest.fixture
def converter(mock_driver):
    return CurrencyConverter(mock_driver)


@patch("src.currency_converter.WebDriverWait")
def test_convert_currency_success(MockWebDriverWait, converter: CurrencyConverter):
    """
    Test the convert_currency method for successful conversion.
    """
    mock_wait = MockWebDriverWait.return_value
    mock_wait.until.side_effect = [
        MagicMock(),  # For initial page load
        MagicMock(),  # For cookie consent
        MagicMock(),  # For base currency input
        MagicMock(),  # For quote currency input
        MagicMock(get_attribute=MagicMock(return_value="1.23")),  # For rate element
    ]

    rate, error = converter.convert_currency("GBP", "EUR")

    assert rate == 1.23
    assert error is None


@patch("src.currency_converter.WebDriverWait")
def test_convert_currency_failure(MockWebDriverWait, converter: CurrencyConverter):
    """
    Test the convert_currency method for failure in conversion.
    """
    mock_wait = MockWebDriverWait.return_value
    mock_wait.until.side_effect = Exception("Some error")

    rate, error = converter.convert_currency("ZZZ", "EUR")

    assert rate is None
    assert isinstance(error, Error)
    assert str(error) == "Error: Failed to convert currency."


@patch("src.currency_converter.WebDriverWait")
def test_handle_cookie_consent(MockWebDriverWait, converter: CurrencyConverter):
    """
    Test the _handle_cookie_consent method.
    """
    mock_wait = MockWebDriverWait.return_value
    mock_cookie_button = MagicMock()
    mock_wait.until.return_value = mock_cookie_button

    converter._handle_cookie_consent()

    mock_cookie_button.click.assert_called_once()


@patch("src.currency_converter.WebDriverWait")
def test_set_currency_input(MockWebDriverWait, converter: CurrencyConverter):
    """
    Test the _set_currency_input method.
    """
    mock_wait = MockWebDriverWait.return_value
    mock_input_field = MagicMock()
    mock_wait.until.return_value = mock_input_field

    converter._set_currency_input("GBP", "baseCurrency_currency_autocomplete")

    mock_input_field.click.assert_called_once()
    mock_input_field.send_keys.assert_any_call(Keys.COMMAND + "a")
    mock_input_field.send_keys.assert_any_call(Keys.BACKSPACE)
    mock_input_field.send_keys.assert_any_call("GBP")
    mock_input_field.send_keys.assert_any_call(Keys.ARROW_DOWN)
    mock_input_field.send_keys.assert_any_call(Keys.RETURN)
