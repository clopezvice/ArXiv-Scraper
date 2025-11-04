"""
url_finder.py
-------------

This module provides a utility function to dynamically build advanced search URLs 
for the arXiv website based on specific parameters such as category, date range, 
and pagination. It adapts automatically for physics and non-physics categories 
using predefined configuration mappings.

Authors:
    - Alejandro Cano Jones (acanojo@uoc.edu)
    - Christian López (clopezvice@uoc.edu)

Subject:
    M2.851 - Tipología y ciclo de vida de los datos. Master in Data Science (UOC)
"""

# --- Import necessary constants from the configuration module ---
try:
    from arxivescrapper.config.config import ARXIV_BASE_URL, PHYSICS_CATEGORIES, NON_PHYSICS_MAP
except Exception:
    # Handle relative import issues when executed from different environments (e.g., Colab)
    import os
    import sys

    _this = os.path.abspath(__file__)
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_this)))
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

    from arxivescrapper.config.config import ARXIV_BASE_URL, PHYSICS_CATEGORIES, NON_PHYSICS_MAP


def get_url(start_date: str = '2025-01-01', end_date: str = '2025-02-01', category: str = 'gr-qc', start: int = 0, cross_list: bool = False) -> str:
    """
    Builds an advanced search URL for arXiv based on the given parameters.

    Args:
        start_date (str): The start date of the search range in YYYY-MM-DD format.
        end_date (str): The end date of the search range in YYYY-MM-DD format.
        category (str): The main arXiv category (e.g., 'gr-qc', 'math', 'cs').
        start (int): Index of the first result to fetch (for pagination).
        cross_list (bool): Whether to include cross-listed papers (True/False).

    Returns:
        str: A fully formatted URL string ready to be used in an HTTP request.

    Example:
        >>> url = get_url('2025-09-01', '2025-11-01', 'cs', start=200, cross_list=True)
        >>> print(url)
        https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND...
    """

    # Initialize the base of the advanced search query
    query_url = ARXIV_BASE_URL + "/search/advanced?"
    query_url += "advanced=1&terms-0-operator=AND&terms-0-term=&terms-0-field=title&"

    # Define category type (physics vs non-physics)
    if category in PHYSICS_CATEGORIES:
        # Physics categories use a specific parameter name
        query_url += f"classification-physics=y&classification-physics_archives={category}"
    else:
        # Map non-physics categories (e.g., 'math' -> 'mathematics')
        classification = NON_PHYSICS_MAP.get(category)
        query_url += f"classification-{classification}=y"
        
    # Include or exclude cross-listed papers
    query_url += f"&classification-include_cross_list={"include" if cross_list else "exclude"}&"
    
    # Add date range, sorting, and pagination options
    query_url += f"date-year=&date-filter_by=date_range&date-from_date={start_date}&date-to_date={end_date}&date-date_type=announced_date_first&"
    query_url += f"abstracts=show&size=200&order=-announced_date_first&start={start}"
    return query_url



if __name__ == "__main__":
    print("This module works out to build arXiv search URLs based on given parameters.")
