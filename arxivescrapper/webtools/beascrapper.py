"""
beascrapper.py
--------------

This module provides utility functions for fetching and parsing HTML content
from arXiv pages (or other websites) using the `requests` library and BeautifulSoup.

It defines a single function, `get_soup()`, which retrieves the HTML content
from a given URL, handles possible HTTP errors, and returns a parsed BeautifulSoup object.

Authors:
    - Alejandro Canojo (acanojo@uoc.edu)
    - Christian López (clopezvice@uoc.edu)

Subject:
    M2.851 - Tipología y ciclo de vida de los datos. Master in Data Science (UOC)
"""


import requests
from bs4 import BeautifulSoup


# ---------------------------------------------------------------------
# Import global request headers from the configuration module.
# If the import fails (e.g., due to path issues in Google Colab),
# the script adjusts the Python path dynamically.
# ---------------------------------------------------------------------

try:
    from arxivescrapper.config.config import REQUESTS_HEADER
except Exception:
    import os
    import sys

    _this = os.path.abspath(__file__)
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_this)))
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

    from arxivescrapper.config.config import REQUESTS_HEADER


# ---------------------------------------------------------------------
# HTML Retrieval and Parsing Function
# ---------------------------------------------------------------------

def get_soup(url: str) -> BeautifulSoup | None:
    """
    Fetches and parses the HTML content of a given URL using BeautifulSoup.

    This function sends an HTTP GET request to the specified URL with
    the configured headers. If the request is successful (status code 200),
    it returns a BeautifulSoup object representing the parsed HTML document.

    Args:
        url (str): The full URL of the page to scrape.

    Returns:
        BeautifulSoup | None:
            - BeautifulSoup object if the request was successful.
            - None if an error occurred.

    Raises:
        ConnectionError: If the request fails or returns a non-200 status code.

    Example:
        >>> soup = get_soup("https://arxiv.org/search/advanced?
        advanced=&terms-0-operator=AND&terms-0-term=&terms-0-field=title&classification-mathematics=y&
        classification-physics=y&classification-physics_archives=all&classification-include_cross_list=include&
        date-year=&date-filter_by=date_range&date-from_date=2025-09-01&date-to_date=2025-11-01&
        date-date_type=announced_date_first&abstracts=show&size=50&order=-announced_date_first")
        >>> print(soup.title.string)
    """
    try:
        response = requests.get(url, headers=REQUESTS_HEADER)
        
        # Ensure the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            return soup

        # Raise an explicit error for unexpected status codes
        else:
            raise ConnectionError(f"Failed to retrieve URL: {url} with status code {response.status_code}")
    except requests.RequestException as e:
        raise ConnectionError(f"An error occurred while fetching the URL: {url}. Error: {e}")
