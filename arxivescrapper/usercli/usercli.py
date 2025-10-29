import argparse
import datetime

try:
    from arxivescrapper.config.config import CATEGORIES
except Exception:
    import os
    import sys

    _this = os.path.abspath(__file__)
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_this)))
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

    from arxivescrapper.config.config import CATEGORIES



def check_dates(start_date: str, end_date: str) -> bool:

    try:
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        return start <= end
    except ValueError:
        return False


def check_categories(category: str) -> bool:

    if category in CATEGORIES:
        return True
    return False


def check_output_path(output_path: str) -> None:

    directory = os.path.dirname(output_path)
    if directory and not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)


def validate_inputs(args) -> None:

    if not check_dates(args.start_date, args.end_date):
        raise ValueError("Invalid date range provided.")
    if not check_categories(args.category):
        raise ValueError("Invalid category provided.")
    check_output_path(args.output)


def parse_arguments():

    parser = argparse.ArgumentParser(description="ArXiv Scraper. Scrapes ArXiv for papers within a date range.")
    parser.add_argument("--start_date", type=str, required=True, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end_date", type=str, required=True, help="End date in YYYY-MM-DD format")
    parser.add_argument("--category", type=str, required=True, help="Category to filter by")
    parser.add_argument("--cross_list", action="store_true", help="Include cross-listed papers")
    parser.add_argument("--output", type=str, nargs="?", default="arxiv_data.csv", help="Output CSV file path")
    
    args = parser.parse_args()
    validate_inputs(args)

    return args

if __name__ == "__main__":
    print("This module provides a CLI for validating user inputs for the ArXiv scraper.")