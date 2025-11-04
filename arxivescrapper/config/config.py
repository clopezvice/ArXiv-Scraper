"""
config.py
----------

This module defines all global configuration constants used throughout the
**arxivescrapper** project. It includes:

- arXiv subject categories (physics and non-physics)
- Mapping for non-physics category names
- Base URL for the arXiv website
- Custom HTTP headers for `requests` sessions

Authors:
    - Alejandro Cano Jones (acanojo@uoc.edu)
    - Christian López (clopezvice@uoc.edu)

Subject:
    M2.851 - Tipología y ciclo de vida de los datos. Master in Data Science (UOC)
"""


# ------------------------------------------------------------------------------------
# arXiv CATEGORIES
# ------------------------------------------------------------------------------------

# Complete list of arXiv subject categories, including both physical and non-physical areas.
CATEGORIES = {"astro-ph", "cond-mat", "gr-qc", "hep-ex", "hep-lat", "hep-ph", "hep-th",
                        "math-ph", "nlin", "nucl-ex", "nucl-th", "physics", "quant-ph", "math", "cs",
                        "q-bio", "q-fin", "stat", "eess", "econ"}

# Subset of categories specifically related to physics.
PHYSICS_CATEGORIES = {"astro-ph", "cond-mat", "gr-qc", "hep-ex", "hep-lat", "hep-ph", "hep-th",
                        "math-ph", "nlin", "nucl-ex", "nucl-th", "physics", "quant-ph"}


# ------------------------------------------------------------------------------------
# NON-PHYSICS CATEGORY MAPPING
# ------------------------------------------------------------------------------------

# This dictionary provides human-readable names for non-physics arXiv categories.
NON_PHYSICS_MAP = {
    "math": "mathematics",
    "cs": "computer-science",
    "q-bio": "q_biology",
    "q-fin": "q_finance",
    "stat": "statistics",
    "eess": "eess",
    "econ": "economics"
}


# ------------------------------------------------------------------------------------
# NETWORK AND HTTP HEADERS CONFIGURATION
# ------------------------------------------------------------------------------------

# Base URL for all arXiv web requests.
ARXIV_BASE_URL = "https://arxiv.org"

# Custom headers used for making polite web requests to arXiv.
# The 'From' field includes both authors’ emails as contact points.
REQUESTS_HEADER = {
    "User-Agent": "UOC Data Science scrapper bot.",
    "From": "acanojo@uoc.edu, clopezvice@uoc.edu",
    "Accept-Language": "en, es-ES;q=0.9"
}


# ------------------------------------------------------------------------------------
# MODULE ENTRY POINT
# ------------------------------------------------------------------------------------

# If this file is executed directly, print an informational message.
if __name__ == "__main__":
    print("This module defines configuration constants.")
