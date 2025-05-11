import time
from typing import Tuple, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from src.error import Error


codes = {
    "GBP": "British Pound",
    "TRY": "Turkish Lira",
    "EUR": "Euro",
}


class CurrencyConverter:
    """
    A class to handle currency conversion using the OANDA currency converter.
    This class uses Selenium to automate the process of converting currency on the OANDA website.
    """

    URL = "https://www.oanda.com/currency-converter/en/"
    WAIT_SECONDS = 10
    AUTOCOMPLETE_ROOT_SELECTOR = ".MuiAutocomplete-root"
    BASE_CURRENCY_INPUT_ID = "baseCurrency_currency_autocomplete"
    QUOTE_CURRENCY_INPUT_ID = "quoteCurrency_currency_autocomplete"
    RATE_INPUT_ID = "input[name='numberformat'][tabindex='4']"
    COOKIE_ID = "onetrust-accept-btn-handler"

    def __init__(self, driver: webdriver.Chrome):
        """
        Initialize the CurrencyConverter with a Selenium WebDriver instance.

        Args:
            driver (webdriver.Chrome): The Selenium WebDriver instance to use for automation.
        """
        self.driver = driver()

    def convert_currency(
        self, from_currency: str, to_currency: str = "EUR"
    ) -> Tuple[Optional[float], Optional[Error]]:
        """
        Convert currency using the OANDA currency converter.

        Args:
            from_currency (str): The currency code to convert from.
            to_currency (str): The currency code to convert to. Default is "EUR".

        Returns:
            Tuple[Optional[float], Optional[Error]]: A tuple containing the converted amount (or None if not found)
                                                     and an error message (or None if no error occurs).

        Raises:
            Exception: If there is an error during the conversion process.
        """
        try:
            self.driver.get(self.URL)

            # Wait for the homepage to load and the currency input fields to be present
            self._webdriver_wait().until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.AUTOCOMPLETE_ROOT_SELECTOR)
                )
            )

            # Wait for the cookie consent button to be clickable and click it
            self._handle_cookie_consent()

            # Wait for the BASE currency input fields to be present
            self._set_currency_input(from_currency, self.BASE_CURRENCY_INPUT_ID)

            # Wait for the QUOTE currency input fields to be present
            self._set_currency_input(to_currency, self.QUOTE_CURRENCY_INPUT_ID)

            # Wait for the conversion to complete
            time.sleep(4)

            # Wait for the rate input field to be present and retrieve the value
            rate_element = self._webdriver_wait().until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.RATE_INPUT_ID))
            )
            rate_value = rate_element.get_attribute("value")

            return float(rate_value), None

        except Exception:
            return None, Error("Failed to convert currency.")

        finally:
            self.driver.quit()

    def _handle_cookie_consent(self):
        """
        Handle cookie consent for the OANDA website.
        """
        cookie_accept_button = self._webdriver_wait().until(
            EC.element_to_be_clickable((By.ID, self.COOKIE_ID))
        )
        cookie_accept_button.click()

    def _set_currency_input(self, currency_code: str, web_element: str):
        """
        Set the currency input field with the desired currency code.

        Args:
            currency_code (str): The currency code to set.
            web_element (str): The ID of the web element to interact with.
        """
        input_field = self._webdriver_wait().until(
            EC.element_to_be_clickable((By.ID, web_element))
        )
        input_field.click()  # Click to focus
        input_field.send_keys(Keys.COMMAND + "a")  # Select all text
        input_field.send_keys(Keys.BACKSPACE)  # Clear the field
        input_field.send_keys(currency_code)  # Enter the desired currency code
        input_field.send_keys(
            Keys.ARROW_DOWN
        )  # Press the down arrow key to select the first suggestion
        input_field.send_keys(Keys.RETURN)  # Confirm the selection

        # Additional checks
        actual_value = input_field.get_attribute("value")
        expected_value = codes.get(currency_code)
        if actual_value != expected_value:
            print(f"Expected {expected_value} but got {actual_value}")

    def _webdriver_wait(self) -> WebDriverWait:
        """
        WebDriver instance with timeout.

        Returns:
            WebDriverWait: The WebDriverWait instance for the specified element.
        """
        return WebDriverWait(self.driver, self.WAIT_SECONDS)
