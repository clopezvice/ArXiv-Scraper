"""
ArXiv Scraper
Is not feasable to scrape all data at once, so we limit to 500 results for testing.
Scrapes ArXiv for papers within a date range for all categories.
It should only scrape specified categories, but this is not implemented.
Should add an option to add cross-list categories, and by default not include them (less data).
Include DOI if available (NONE if not).
"""

import requests
from bs4 import BeautifulSoup, element
import re
import pandas as pd
import argparse
from tqdm import tqdm
from time import sleep

def parse_arguments():
    parser = argparse.ArgumentParser(description="ArXiv Scraper. Scrapes ArXiv for papers within a date range.")
    parser.add_argument("--start_date", type=str, required=True, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end_date", type=str, required=True, help="End date in YYYY-MM-DD format")
    parser.add_argument("--output", type=str, nargs="?", default="arxiv_data.csv", help="Output CSV file path")
    parser.add_argument("--categories", type=str, nargs="*", help="Categories to filter by (not implemented)")
    return parser.parse_args()

def get_URL(start_date: str, end_date: str, start_index: int = 0) -> str:
    # Must implement categories filtering
    base_url = "https://arxiv.org/search/advanced?"
    URL = (
        f"{base_url}"
        f"advanced=&terms-0-operator=AND&terms-0-term=&terms-0-field=title&"
        f"classification-physics_archives=all&classification-include_cross_list=include&"
        f"date-year=&"
        f"date-from_date={start_date}&date-to_date={end_date}&"
        f"date-date_type=announced_date_first&abstracts=show&"
        f"size=50&order=-announced_date_first&"
        f"start={start_index}"
    )
    return URL

def get_index(result: element.Tag) -> str:
    idx = result.select_one('p.list-title').get_text(strip=True)
    idx = idx.split(':')[1].split('[')[0]
    return idx

def get_title(result: element.Tag) -> str:
    return result.select_one('p.title').get_text(strip=True)

def get_tags(result: element.Tag) -> list[str]:
    tag_list = []
    for tag in result.select('span.tag'):
        tag_list.append(tag.get_text(strip=True))
    return tag_list

def get_authors(result: element.Tag) -> list[str]:
    author_list = []
    for author in result.select('p.authors a'):
        author_list.append(author.get_text(strip=True))
    return author_list

def get_abstract(result: element.Tag) ->str:
    abstract_full = result.select_one('p.abstract span.abstract-full')
    for link in abstract_full.select('a'):
        link.decompose()
    abstract = abstract_full.get_text(strip=True)
    return abstract

def number_of_results(soup: BeautifulSoup) -> int | None:
    result_number = soup.select_one('h1.title.is-clearfix').get_text(strip=True)
    match = re.search(r'of ([0-9,]+) results', result_number)
    if match:
        total_results = int(match.group(1).replace(',', ''))
        return total_results
    return None

headers = {
    "User-Agent": "UOC Data Science scrapper bot.",
    "From": "acanojo@uoc.edu",
    "Accept-Language": "en, es-ES;q=0.9"
}



if __name__ == "__main__":

    args = parse_arguments()
    URL = get_URL(args.start_date, args.end_date)

    request = requests.get(URL, headers=headers)
    request.raise_for_status()
    soup = BeautifulSoup(request.text, "html.parser")
    total_results = number_of_results(soup)
    print(f"Total results found: {total_results}")

    data = {
            "index": [],
            "title": [],
            "tags": [],
            "authors": [],
            "abstract": []
        }

    # list_indexes = [i for i in range(0, total_results, 50)]
    list_indexes = [i for i in range(0, 500, 50)]
    for start_index in tqdm(list_indexes, desc="Scraping pages"):
        URL = get_URL(args.start_date, args.end_date, start_index=start_index)
        request = requests.get(URL, headers=headers)
        request.raise_for_status()
        soup = BeautifulSoup(request.text, "html.parser")

        

        for result in soup.select('li.arxiv-result'):
            data["index"].append(get_index(result))
            data["title"].append(get_title(result))
            data["tags"].append(get_tags(result))
            data["authors"].append(get_authors(result))
            data["abstract"].append(get_abstract(result))
        
        sleep(15)

    df = pd.DataFrame(data)
    df.to_csv(args.output, index=False)


    