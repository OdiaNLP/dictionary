from dictionary.lang_detector import check_odia_text
import json

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from nltk.stem import WordNetLemmatizer


app = FastAPI()
with open("./data/Odia_structured_wordlist.json", "r") as fh:
    word_dict = json.load(fh)

with open("./data/cleaned_pairs.json") as translated_handler:
    en_or_dict = json.load(translated_handler)

@app.post("/translate/")
async def search(text_field: str = Form(...)):
    if check_odia_text(text_field):
        # Odia input text asked
        if text_field in word_dict:
            translation = {
                "odia_text": text_field,
                "meaning": word_dict[text_field]["word_details"]
            }
        else:
            translation = {
                "ବାର୍ତ୍ତା": f"କ୍ଷମା କରିବେ । '<b>{text_field}</b>' ଶବ୍ଦଟିର ଅର୍ଥ ଯୋଗାଇବାକୁ ମୁଁ ଅସମର୍ଥ ।"
            }
    else:
        # English input text processor
        lemmatizer = WordNetLemmatizer()
        en_text = lemmatizer.lemmatize(text_field, pos="n")
        en_text = lemmatizer.lemmatize(en_text, pos="a")
        en_text = lemmatizer.lemmatize(en_text, pos="v")
        if en_text in en_or_dict:
            translation =  {
                "english-text": text_field,
                "odia-text": en_or_dict[en_text]
            }
        else:
            meaning = {}
            # breakpoint()
            for words in en_or_dict.keys():
                if set([en_text]).intersection(set(words.split())):
                    meaning[words] = en_or_dict[words]
            if meaning:
                translation = {
                    "english-text": text_field,
                    "odia-text": meaning
                }
            else:
                translation = {
                    "message": f"I am sorry. Unable to find the Odia of the word: <b>'{text_field}'</b>"
                }
    translation_content = json.dumps(translation, ensure_ascii=False, indent=4)
    print(translation_content)
    content = """
            <body>
            <form action="/translate/" enctype="multipart/form-data" method="post">
            <input name="text_field" type=str """ + f'placeholder={text_field}' + \
            """
            <input type="submit">
            </form>
            </body>
            """ + translation_content
    return HTMLResponse(content=content)


@app.get("/")
async def home():
    content = """
        <body>
        <form action="/translate/" enctype="multipart/form-data" method="post">
        <input name="text_field" type=str >
        <input type="submit">
        </form>
        </body>
        """
    return HTMLResponse(content=content)
