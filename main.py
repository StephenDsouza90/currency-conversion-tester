from typing import Optional

from selenium import webdriver

from src.currency_utils import get_currency_rate, check_threshold


def main(country_code: str, threshold: int) -> Optional[bool]:
    """
    Main function to run the currency conversion and threshold check.

    Args:
        country_code (str): The ISO 3166-1 alpha-2 country code.
        threshold (int): The threshold value to check against the exchange rate.

    Returns:
        Optional[bool]: True if the exchange rate is above the threshold, False otherwise.
                        Returns None if there is an error during the process.
    """
    rate, currency, error = get_currency_rate(webdriver.Chrome, country_code)

    if error:
        return None

    is_threshold_met = check_threshold(rate, threshold)

    if is_threshold_met:
        print(f"Exchange rate for {currency} is higher than {threshold}.")
    else:
        print(f"Exchange rate for {currency} is not higher than {threshold}.")

    return is_threshold_met


if __name__ == "__main__":
    country_codes = ["TR", "GB"]
    threshold = 1

    for country_code in country_codes:
        main(country_code, threshold)
