from typing import Optional, Tuple

from selenium import webdriver

from src.country_info import CountryInfo
from src.currency_converter import CurrencyConverter
from src.error import Error


def get_currency_rate(
    driver: webdriver,
    country_code: str,
) -> Tuple[Optional[float], Optional[str], Optional[Error]]:
    """
    Retrieve the currency exchange rate for a given country code.

    Args:
        driver (webdriver): The Selenium WebDriver instance.
        country_code (str): The ISO 3166-1 alpha-2 country code.

    Returns:
        Optional[float]: The exchange rate if successful, None otherwise.
        Optional[str]: The currency code if successful, None otherwise.
        Optional[Error]: An error object if an error occurs, None otherwise.
    """
    currency, error = CountryInfo().run(country_code)

    if error:
        return None, currency, error

    rate, error = CurrencyConverter(driver).convert_currency(currency)

    if error:
        return None, currency, error

    return rate, currency, None


def check_threshold(rate: float, threshold: int) -> bool:
    """
    Check if the exchange rate is above a certain threshold.

    Args:
        rate (float): The exchange rate to check.
        threshold (float): The threshold value.

    Returns:
        bool: True if the rate is above the threshold, False otherwise.
    """
    return rate > threshold
