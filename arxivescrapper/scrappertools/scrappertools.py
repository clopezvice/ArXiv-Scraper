from bs4 import BeautifulSoup, element
import re


def number_of_results(soup: BeautifulSoup) -> int | None:
    result_number = soup.select_one('h1.title.is-clearfix').get_text(strip=True)
    match = re.search(r'of ([0-9,]+) results', result_number)
    if match:
        total_results = int(match.group(1).replace(',', ''))
        return total_results
    return None

def get_index(result: element.Tag) -> str:
    idx = result.select_one('p.list-title').get_text(strip=True)
    idx = idx.split(':')[1].split('[')[0]
    return idx

def get_title(result: element.Tag) -> str:
    return result.select_one('p.title').get_text(strip=True)

def get_tags(result: element.Tag) -> list[str]: #sometimes includes doi, gotta filter that out
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