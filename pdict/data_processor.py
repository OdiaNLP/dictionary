from bs4 import BeautifulSoup
import pickle

    # soup = BeautifulSoup(response.content, "html.parser", from_encoding="utf-8")
    # div = soup.find("div", {"class": "hw_result"})
    # entries = div.find_all('entry')
    # odia_sentences = [each_odia_entry.text for entry in entries for each_odia_entry in entry.find_all('or')]
    # print("odia_sentences: ", odia_sentences)
    # english_sentences = [each_odia_entry.text for entry in entries for each_odia_entry in entry.find_all('tr')]
    # print("english_sentences: ", english_sentences)
    # hindi_sentences = [each_odia_entry.text for entry in entries for each_odia_entry in entry.find_all('d')]
    # print("hindi_sentences: ", hindi_sentences)
    # bengali_sentences = [each_odia_entry.text for entry in entries for each_odia_entry in entry.find_all('be')]
    # print("bengali_sentences: ", bengali_sentences)

with open("./data/full_dump.txt", 'rb') as fh:
    content_list = pickle.load(fh)
print(len(content_list))
