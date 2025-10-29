from usercli.usercli import parse_arguments
from webtools.url_finder import get_url
from webtools.beascrapper import get_soup
from scrappertools.scrappertools import *

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

    first_url = get_url(start_date=start_date, end_date=end_date, category=category, cross_list=cross_list)
    soup = get_soup(first_url)

    total_results = number_of_results(soup)
    if total_results is None:
        raise ValueError("No results found or unable to parse the number of results.")

    print(f"Total results found: {total_results}")

    page_indexes = [i for i in range(0, total_results, 200)]

    data = {
        "index": [],
        "title": [],
        "tags": [],
        "authors": [],
        "abstract": []
    }

    for start in tqdm(page_indexes, desc="Scraping pages"):
        url = get_url(start_date=start_date, end_date=end_date, category=category, start=start, cross_list=cross_list)
        soup = get_soup(url)
        results = soup.select('li.arxiv-result')

        for result in results:
            data["index"].append(get_index(result))
            data["title"].append(get_title(result))
            data["tags"].append(get_tags(result))
            data["authors"].append(get_authors(result))
            data["abstract"].append(get_abstract(result))

        sleep(15)  # polite delay to avoid overwhelming the server

    dataframe = DataFrame(data)
    dataframe.to_csv(output, index=False)
    print(f"Data saved to {output}")
    return dataframe


def main(argv=None):

    if argv is None:
        args = parse_arguments()
        start_date = args.start_date
        end_date = args.end_date
        category = args.category
        output = getattr(args, 'output', 'arxiv_data.csv')
        cross_list = getattr(args, 'cross_list', False)

    elif isinstance(argv, Mapping):
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

    return scrape_arxiv(start_date=start_date,
                        end_date=end_date,
                        category=category,
                        output=output,
                        cross_list=cross_list)


if __name__ == "__main__":
    main()
