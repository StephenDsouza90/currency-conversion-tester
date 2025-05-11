import json
from typing import Tuple, Optional

import requests

from src.error import Error

codes = {
    "GB": "GBP",
    "TR": "TRY",
}


class CountryInfo:
    """
    A class to fetch and extract country information, including currency details.
    """

    @staticmethod
    def fetch_country_info(country_code: str) -> requests.Response:
        """
        Fetch country information for a given country code.

        Args:
            country_code (str): The ISO 3166-1 alpha-2 country code.

        Returns:
            requests.Response: The response object containing country information.
        """
        return requests.get(f"https://restcountries.com/v3.1/alpha/{country_code}")

    @staticmethod
    def extract_currency(
        country_response: requests.Response,
    ) -> Tuple[Optional[str], Optional[Error]]:
        """
        Extract currency information from the country response.

        Args:
            country_response (requests.Response): The response object containing country information.

        Returns:
            Tuple[Optional[str], Optional[Error]]: A tuple containing the currency code (or None if not found)
                                                   and an error message (or None if no error occurs).
        """
        try:
            if country_response.status_code != 200:
                error_message = country_response.json().get("message")
                return None, Error(error_message)

            country_data = country_response.json()
            currency_data = country_data[0].get("currencies")
            if not currency_data:
                return None, Error("No currency data found.")

            currency = list(currency_data.keys())[0]
            if len(currency) != 3:
                return None, Error("Invalid currency code format.")

            return currency, None

        except (IndexError, json.JSONDecodeError):
            return None, Error("Invalid response format.")

        except AttributeError:
            return None, Error("API response format changed.")

        except Exception as e:
            return None, Error(str(e))

    def run(self, country_code: str) -> Tuple[Optional[str], Optional[Error]]:
        """
        Main function to fetch and extract currency information for a given country code.

        Args:
            country_code (str): The ISO 3166-1 alpha-2 country code.

        Returns:
            Tuple[Optional[str], Optional[Error]]: A tuple containing the currency code (or None if not found)
                                                   and an error message (or None if no error occurs).
        """
        country_response = self.fetch_country_info(country_code)
        currency, error = self.extract_currency(country_response)

        # Additional checks
        expected_currency = codes.get(country_code)
        if expected_currency != currency:
            return None, Error(f"Expected {expected_currency} but got {currency}")

        return currency, error
