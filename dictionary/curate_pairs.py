"""
@author: Soumendra Kumar Sahoo
@date: August 2021
@function: Process English to Odia language word translations
@license: MIT License
"""
import json

with open("./data/translated.txt") as fh:
    word_pairs = fh.readlines()
try:
    output_json = {}
    for word_pair in word_pairs:
        word_pair = word_pair.rstrip(" |\n")
        en_word, or_word = word_pair.split("||")
        output_json[en_word] = or_word
except Exception:
    print(word_pair, word_pair.split("||"))
# Serializing json
json_object = json.dumps(output_json, indent=4, ensure_ascii=False)

# Writing to sample.json
with open("./data/cleaned_pairs.json", "w") as wfh:
    wfh.write(json_object)

# with open("./data/Odia_structured_wordlist.json", "r+") as fh:
#     all_words = json.load(fh)
#     for all_word in all_words:
#         del all_words[all_word]['raw']
#     all_words = json.dumps(all_words, indent=4, ensure_ascii=False)
#     fh.write(all_words)