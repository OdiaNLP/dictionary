"""
@author: Soumendra Kumar Sahoo
@date: August 2021
@function: Process English to Odia language word translations
@license: MIT License
"""

ODIA_MATRA = {
    "ଁ",
    "ଂ",
    "ଃ",
    "଼",
    "ଽ",
    "ା",
    "ି",
    "ୀ",
    "ୁ",
    "ୂ",
    "ୃ",
    "ୄ",
    "େ",
    "ୈ",
    "ୋ",
    "ୌ",
    "୍",
    "ୖ",
    "ୗ",
    "୰",
    "ୱ",
    "୲",
}


def check_odia_text(text):
    """ Odia language detector """
    return bool(any(matra in text for matra in ODIA_MATRA))
