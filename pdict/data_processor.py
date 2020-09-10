"""
Author: Soumendra Kumar Sahoo
Start date: 11th August 2020
This module processes the web page details after it's downloaded.
Due to more than 100MB size of the file.  I am unable to add the file to GitHub.
"""
import json
import pickle
from collections import defaultdict
from sys import getsizeof

from bs4 import BeautifulSoup

with open("./data/full_dump.txt", "rb") as fh:
    content_list = pickle.load(fh)
print("Pages extracted: ", len(content_list))
final_word_dict = defaultdict(dict)
for i, each_page in enumerate(content_list, 1):
    print(f"processing for page: {i}")
    if not each_page[0]:
        print("ERROR: ", i, each_page)
        continue
    soup = BeautifulSoup(each_page[0], "html.parser")
    div = soup.find("div", {"class": "hw_result"})
    entries = div.find_all("entry")
    for each_word in entries:
        word = each_word.find("or").text.strip()
        final_word_dict[word]["raw"] = each_word and each_word.text
        final_word_dict[word]["pronunciation"] = each_word.find("tr") and each_word.find("tr").text
        final_word_dict[word]["gender"] = (
            each_word.find("gender") and each_word.find("gender").text
        )
        final_word_dict[word]["synonyms"] = each_word.find("syn") and each_word.find("syn").text
        multi_meanings = each_word.find_all("gramgrp")
        word_list = []
        for each_meaning in multi_meanings:
            word_details = {
                "verse": each_meaning.find("verse") and each_meaning.find("verse").text,
                "meaning": each_meaning.find("sense") and each_meaning.find("sense").text,
                "juktakhyara": each_meaning.find_all("or") and each_meaning.find_all("or")[0].text,
            }
            word_list.append(word_details)
        final_word_dict[word]["word_details"] = word_list

with open("./data/Odia_structured_wordlist.json", "w+") as sw:
    json.dump(final_word_dict, sw, ensure_ascii=False, sort_keys=True, indent=2)
print(len(final_word_dict))
print("Dictionary size: ", getsizeof(json.dumps(final_word_dict)))
