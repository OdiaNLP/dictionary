"""
@author: Soumendra Kumar Sahoo
@date: August 2021
@function: Process English to Odia language word translations
@license: MIT License
"""
from dictionary.lang_detector import check_odia_text
from googletrans import Translator
from time import sleep
from random import randrange
from nltk.stem import WordNetLemmatizer


translator = Translator()


class En2Or:
    def read_file(self):
        with open("./data/en.txt") as en_fh:
            english_words = en_fh.readlines()
        return english_words

    def lemmatize_text(self, english_words):
        lemmatizer = WordNetLemmatizer()
        final_en_words = set()
        for en_word in english_words:
            temp_word = lemmatizer.lemmatize(en_word, pos="n")
            temp_word = lemmatizer.lemmatize(temp_word, pos="a")
            temp_word = lemmatizer.lemmatize(temp_word, pos="v")
            final_en_words.add(temp_word)
        print(
            f"Lemmatization completed the final en word count: {len(final_en_words)} "
            f"from original word count: {len(english_words)}"
        )
        self.write_file("./data/cleaned_en.txt", final_en_words)
        return final_en_words

    def write_file(self, filename, written_words, mode="w+"):
        print(f"writing file: {filename} with {len(written_words)} words")
        if isinstance(written_words, set):
            written_words = "".join(written_words)
        with open(filename, mode) as write_fh:
            write_fh.write(written_words)

    def translate(self, final_en_words):
        odia_words = set()
        for cnt, en_word in enumerate(final_en_words):
            try:
                temp_odia_word = translator.translate(en_word, dest="or").text
                if not check_odia_text(temp_odia_word):
                    print(f"{temp_odia_word} is not a valid odia word")
                    continue
                temp_odia_word = f"{en_word.strip()}||{temp_odia_word.rstrip(' |')}\n"
                print(cnt, temp_odia_word)
                odia_words.add(temp_odia_word)
            except Exception as err:
                print(f"Error: {err}")
                self.write_file("./data/translated.txt", odia_words, mode="a+")
                sleep(120)
                odia_words = set()


if __name__ == "__main__":
    english_to_odia = En2Or()
    english_words = english_to_odia.read_file()
    final_en_words = english_to_odia.lemmatize_text(english_words)
    english_to_odia.translate(final_en_words)
    # english_to_odia.write_file("./data/or.txt", odia_words)
