import requests
from bs4 import BeautifulSoup

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


def get_soup(url: str) -> BeautifulSoup | None:
    try:
        response = requests.get(url, headers=REQUESTS_HEADER)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            return soup
        else:
            raise ConnectionError(f"Failed to retrieve URL: {url} with status code {response.status_code}")
    except requests.RequestException as e:
        raise ConnectionError(f"An error occurred while fetching the URL: {url}. Error: {e}")