"""
scrapertools.py
---------------

Utility functions for extracting structured data from arXiv search result pages
using BeautifulSoup. These functions parse key metadata such as titles, authors,
categories (tags), abstracts, and the total number of results.

This module is part of the UOC Data Science project on web scraping.

Authors:
    Alejandro Cano Jones (acanojo@uoc.edu)
    Christian López Vicente (clopezvice@uoc.edu)
"""

from bs4 import BeautifulSoup, element
import re


def number_of_results(soup: BeautifulSoup) -> int | None:
    """
    Extracts the total number of results from an arXiv search results page.

    Args:
        soup (BeautifulSoup): Parsed HTML of the arXiv search results page.

    Returns:
        int | None: The total number of search results if found, otherwise None.
    """
    # Find the main title element containing the result count text (e.g. "Showing 1–200 of 1,254 results")
    result_number = soup.select_one('h1.title.is-clearfix').get_text(strip=True)

    # Use regex to capture the total number from the text
    match = re.search(r'of ([0-9,]+) results', result_number)
    if match:
        # Remove commas and convert to integer
        total_results = int(match.group(1).replace(',', ''))
        return total_results
    return None

def get_index(result: element.Tag) -> str:
    """
    Extracts the arXiv identifier (e.g., '2507.08819v1') from a search result entry.

    Args:
        result (element.Tag): A single search result block.

    Returns:
        str: The extracted arXiv identifier.
    """
    idx = result.select_one('p.list-title').get_text(strip=True)
    idx = idx.split(':')[1].split('[')[0]
    return idx

def get_title(result: element.Tag) -> str:
    """
    Retrieves the title of an arXiv paper from a search result entry.

    Args:
        result (element.Tag): A BeautifulSoup Tag representing the paper block.

    Returns:
        str: The title text.
    """
    return result.select_one('p.title').get_text(strip=True)

def get_tags(result: element.Tag) -> list[str]:
    """
    Extracts the category tags associated with a paper.
    Filters out 'doi' and DOI numbers (which are sometimes included as tags).

    Args:
        result (element.Tag): A BeautifulSoup Tag for the paper entry.

    Returns:
        list[str]: A list of clean category strings.
    """
    tag_list = []
    for tag in result.select('span.tag'):
        text = tag.get_text(strip=True)
        # Exclude DOI elements
        if text.lower() != 'doi' and not text.startswith('10.'):
            tag_list.append(text)
    return tag_list

def get_authors(result: element.Tag) -> list[str]:
    """
    Extracts all author names from an arXiv paper entry.

    Args:
        result (element.Tag): A BeautifulSoup Tag containing the authors section.

    Returns:
        list[str]: A list of author names.
    """
    author_list = []
    for author in result.select('p.authors a'):
        author_list.append(author.get_text(strip=True))
    return author_list

def get_abstract(result: element.Tag) ->str:
    """
    Extracts the full abstract text from an arXiv search result.

    Removes inline <a> tags used for 'More'/'Less' links.

    Args:
        result (element.Tag): A BeautifulSoup Tag for the paper entry.

    Returns:
        str: The cleaned abstract text.
    """
    # Select the 'full abstract' span (hidden by default in arXiv HTML)
    abstract_full = result.select_one('p.abstract span.abstract-full')

    # Remove any link elements ('More' or 'Less') inside the abstract
    for link in abstract_full.select('a'):
        link.decompose()
        
    # Return the clean text
    abstract = abstract_full.get_text(strip=True)
    return abstract
