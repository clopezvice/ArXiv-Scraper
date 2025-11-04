"""
arxivscraper.py

This module orchestrates the scraping of research papers from arXiv.org
based on user-defined parameters such as date range, category, and cross-list options.
It uses modular helper functions for URL construction, HTML parsing, and data extraction.

Main features:
---------------
- Retrieves metadata (index, title, tags, authors, abstract) for papers in a given category/date range.
- Handles pagination automatically (200 results per page).
- Saves the collected data to a CSV file and returns a Pandas DataFrame.
- Can be executed either via CLI or programmatically by importing the `main()` function.

Modules required:
-----------------
- usercli.usercli         → Parses and validates command-line arguments.
- webtools.url_finder     → Builds search URLs for arXiv queries.
- webtools.beascraper    → Fetches and parses HTML using BeautifulSoup.
- scrapertools.scrapertools → Extracts information from HTML elements.

Authors:
    - Alejandro Cano Jones (acanojo@uoc.edu)
    - Christian López (clopezvice@uoc.edu)

Subject:
    M2.851 - Tipología y ciclo de vida de los datos. Master in Data Science (UOC)
"""

from usercli.usercli import parse_arguments
from webtools.url_finder import get_url
from webtools.beascraper import get_soup
from scrapertools.scrapertools import *

from tqdm import tqdm
from time import sleep
from pandas import DataFrame
from typing import Optional
from collections.abc import Mapping


def scrape_arxiv(start_date: str,
                  end_date: str,
                  category: str,
                  output: str = "arxiv_data.csv",
                  cross_list: bool = False) -> Optional[DataFrame]:
    """
    Scrape arXiv.org for papers in a given category and date range.

    This function retrieves search results from arXiv using the advanced search page,
    parses each result, and extracts metadata such as the paper title, authors,
    index identifier, subject tags, and abstract.

    Parameters
    ----------
    start_date : str
        Start date for the search in 'YYYY-MM-DD' format.
    end_date : str
        End date for the search in 'YYYY-MM-DD' format.
    category : str
        ArXiv category code (e.g., 'gr-qc', 'cs', 'math').
    output : str, optional
        File path to save the results as a CSV file. Defaults to 'arxiv_data.csv'.
    cross_list : bool, optional
        Whether to include cross-listed papers. Defaults to False.

    Returns
    -------
    pandas.DataFrame or None
        A DataFrame containing the scraped data, or None if no data is found.

    Raises
    ------
    ValueError
        If no results are found or if the total number of results cannot be parsed.
    ConnectionError
        If there are issues retrieving pages from arXiv.org.

    Notes
    -----
    - Each page on arXiv lists up to 200 results; this function paginates automatically.
    - A polite delay (15 seconds) is used between page requests to respect arXiv’s servers.
    - The resulting CSV contains columns: 'index', 'title', 'tags', 'authors', 'abstract'.
    """
    
    # Build the first query URL and get the corresponding page (soup)
    first_url = get_url(start_date=start_date, end_date=end_date, category=category, cross_list=cross_list)
    soup = get_soup(first_url)

    # Determine the total number of results from the first page
    total_results = number_of_results(soup)
    if total_results is None:
        raise ValueError("No results found or unable to parse the number of results.")

    print(f"Total results found: {total_results}")
                    
    # Calculate pagination indexes (200 results per page)
    page_indexes = [i for i in range(0, total_results, 200)]
                    
    # Initialize storage for the scraped data
    data = {
        "index": [],
        "title": [],
        "tags": [],
        "authors": [],
        "abstract": []
    }
                    
    # Loop through all result pages
    for start in tqdm(page_indexes, desc="Scraping pages"):
        url = get_url(start_date=start_date, end_date=end_date, category=category, start=start, cross_list=cross_list)
        soup = get_soup(url)
        results = soup.select('li.arxiv-result')
      
        # Extract and append data for each paper in the page
        for result in results:
            data["index"].append(get_index(result))
            data["title"].append(get_title(result))
            data["tags"].append(get_tags(result))
            data["authors"].append(get_authors(result))
            data["abstract"].append(get_abstract(result))
          
        sleep(15)  # polite delay to avoid overwhelming the server
      
    # Convert collected data to a DataFrame and export it to CSV
    dataframe = DataFrame(data)
    dataframe.to_csv(output, index=False)
    print(f"Data saved to {output}")
    return dataframe


def main(argv=None):
    """
    Main entry point for the arXiv scraper.

    This function parses command-line arguments (if run as a script)
    or accepts parameters from a mapping (e.g., a dictionary).
    It then calls `scrape_arxiv()` with the validated arguments.

    Parameters
    ----------
    argv : None | argparse.Namespace | Mapping, optional
        - If None: arguments are read from the command line (default behavior).
        - If Mapping: dictionary-like object containing keys 'start_date', 'end_date', 'category', etc.
        - If argparse.Namespace: arguments parsed via argparse.

    Returns
    -------
    pandas.DataFrame
        The DataFrame returned by `scrape_arxiv()`.

    Raises
    ------
    ValueError
        If required arguments are missing in the Mapping.
    TypeError
        If the provided argv type is unsupported.
    """
    if argv is None:
        # When executed as a script: parse CLI arguments
        args = parse_arguments()
        start_date = args.start_date
        end_date = args.end_date
        category = args.category
        output = getattr(args, 'output', 'arxiv_data.csv')
        cross_list = getattr(args, 'cross_list', False)

    elif isinstance(argv, Mapping):
        # When executed programmatically: use a dictionary-like mapping
        required = ['start_date', 'end_date', 'category']
        missing = [k for k in required if argv.get(k) is None]
        if missing:
            raise ValueError(f"Missing required arguments in mapping passed to main(): {missing}")

        start_date = argv.get('start_date')
        end_date = argv.get('end_date')
        category = argv.get('category')
        output = argv.get('output', 'arxiv_data.csv')
        cross_list = argv.get('cross_list', False)

    else:
        raise TypeError("Unsupported argv type for main(); expected None, argparse.Namespace, or Mapping")
      
    # Run the scraping process
    return scrape_arxiv(start_date=start_date,
                        end_date=end_date,
                        category=category,
                        output=output,
                        cross_list=cross_list)


if __name__ == "__main__":
    main()
