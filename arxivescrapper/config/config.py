

CATEGORIES = {"astro-ph", "cond-mat", "gr-qc", "hep-ex", "hep-lat", "hep-ph", "hep-th",
                        "math-ph", "nlin", "nucl-ex", "nucl-th", "physics", "quant-ph", "math", "cs",
                        "q-bio", "q-fin", "stat", "eess", "econ"}

PHYSICS_CATEGORIES = {"astro-ph", "cond-mat", "gr-qc", "hep-ex", "hep-lat", "hep-ph", "hep-th",
                        "math-ph", "nlin", "nucl-ex", "nucl-th", "physics", "quant-ph"}
NON_PHYSICS_MAP = {
    "math": "mathematics",
    "cs": "computer-science",
    "q-bio": "q_biology",
    "q-fin": "q_finance",
    "stat": "statistics",
    "eess": "eess",
    "econ": "economics"
}

ARXIV_BASE_URL = "https://arxiv.org"

REQUESTS_HEADER = {
    "User-Agent": "UOC Data Science scrapper bot.",
    "From": "acanojo@uoc.edu",
    "Accept-Language": "en, es-ES;q=0.9"
}


if __name__ == "__main__":
    print("This module defines configuration constants.")
