try:
    from arxivescrapper.config.config import ARXIV_BASE_URL, PHYSICS_CATEGORIES, NON_PHYSICS_MAP
except Exception:
    import os
    import sys

    _this = os.path.abspath(__file__)
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_this)))
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

    from arxivescrapper.config.config import ARXIV_BASE_URL, PHYSICS_CATEGORIES, NON_PHYSICS_MAP



def get_url(start_date: str = '2025-01-01', end_date: str = '2025-02-01', category: str = 'gr-qc', start: int = 0, cross_list: bool = False) -> str:
    
    query_url = ARXIV_BASE_URL + "/search/advanced?"
    query_url += "advanced=1&terms-0-operator=AND&terms-0-term=&terms-0-field=title&"
    if category in PHYSICS_CATEGORIES:
        query_url += f"classification-physics=y&classification-physics_archives={category}"
    else:
        classification = NON_PHYSICS_MAP.get(category)
        query_url += f"classification-{classification}=y"

    query_url += f"&classification-include_cross_list={"include" if cross_list else "exclude"}&"
    query_url += f"date-year=&date-filter_by=date_range&date-from_date={start_date}&date-to_date={end_date}&date-date_type=announced_date_first&"
    query_url += f"abstracts=show&size=200&order=-announced_date_first&start={start}"
    return query_url



if __name__ == "__main__":
    print("This module works out to build arXiv search URLs based on given parameters.")