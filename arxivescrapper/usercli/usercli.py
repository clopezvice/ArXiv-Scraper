"""
usercli.py
-----------

This module defines the command-line interface (CLI) for the ArXiv Scraper project.
It handles user input, argument parsing, and validation before executing the scraper.

Functions included:
    - check_dates(): Validates the format and order of date inputs.
    - check_categories(): Ensures the provided category exists in the config.
    - check_output_path(): Verifies or creates the output directory if needed.
    - validate_inputs(): Runs all input checks and raises errors when invalid.
    - parse_arguments(): Builds the CLI, parses user arguments, and validates them.

Authors:
    Alejandro Cano Jones (acanojo@uoc.edu)
    Christian López (clopezvice@uoc.edu)
"""

import argparse
import datetime

# Attempt to import valid categories from configuration.
# If the import fails (e.g., in Google Colab), fix the module path dynamically.
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
    """
    Validates that the provided start and end dates are correctly formatted
    and that the start date is not later than the end date.

    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        bool: True if both dates are valid and in correct order, False otherwise.
    """
    try:
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        return start <= end
    except ValueError:
        return False


def check_categories(category: str) -> bool:
    """
    Validates that the specified category exists in the official arXiv category list.

    Args:
        category (str): Category code (e.g., 'cs.CV', 'math', 'eess.IV').

    Returns:
        bool: True if category is valid, False otherwise.
    """
    if category in CATEGORIES:
        return True
    return False


def check_output_path(output_path: str) -> None:
    """
    Ensures that the directory for the output file exists.
    Creates the directory if it doesn't exist.

    Args:
        output_path (str): Path to the desired output file.
    """
    directory = os.path.dirname(output_path)
    if directory and not os.path.isdir(directory):
        # Create output directory if missing
        os.makedirs(directory, exist_ok=True)


def validate_inputs(args) -> None:
    """
    Runs validation checks for all command-line arguments.
    Raises descriptive errors if any validation fails.

    Args:
        args: Parsed command-line arguments from argparse.

    Raises:
        ValueError: If date range or category is invalid.
    """
    if not check_dates(args.start_date, args.end_date):
        raise ValueError("Invalid date range provided.")
    if not check_categories(args.category):
        raise ValueError("Invalid category provided.")
    check_output_path(args.output)


def parse_arguments():
    """
    Parses and validates command-line arguments for the ArXiv Scraper.

    Returns:
        argparse.Namespace: Object containing validated command-line arguments.
    """
    parser = argparse.ArgumentParser(description="ArXiv Scraper. Scrapes ArXiv for papers within a date range.")
    parser.add_argument("--start_date", type=str, required=True, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end_date", type=str, required=True, help="End date in YYYY-MM-DD format")
    parser.add_argument("--category", type=str, required=True, help="Category to filter by")
    parser.add_argument("--cross_list", action="store_true", help="Include cross-listed papers")
    parser.add_argument("--output", type=str, nargs="?", default="arxiv_data.csv", help="Output CSV file path")

    # Parse and validate user inputs
    args = parser.parse_args()
    validate_inputs(args)

    return args

if __name__ == "__main__":
    print("This module provides a CLI for validating user inputs for the ArXiv scraper.")
