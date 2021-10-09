from typing import Dict
from dictionary.lang_detector import check_odia_text
import json

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from openodia import ud, other_lang_to_odia

from nltk.stem import WordNetLemmatizer


app = FastAPI()
with open("./data/Odia_structured_wordlist.json", "r") as fh:
    word_dict = json.load(fh)

with open("./data/cleaned_pairs.json") as translated_handler:
    en_or_dict = json.load(translated_handler)


def _process_odia_text(text) -> Dict[str, str]:
    """Process the odia text"""
    if text in word_dict:
        translation = {
            "odia_text": text,
            "meaning": word_dict[text]["word_details"]
        }
    else:
        translation = {
            "ବାର୍ତ୍ତା": f"କ୍ଷମା କରିବେ । '<b>{text}</b>' ଶବ୍ଦଟିର ଅର୍ଥ ଯୋଗାଇବାକୁ ମୁଁ ଅସମର୍ଥ ।"
        }
    return translation


def _prepare_content(translation: Dict[str, str], text: str) -> str:
    """Prepare the translation output for UI"""
    translation_content = json.dumps(translation, ensure_ascii=False, indent=4)
    print(translation_content)
    content = """
            <body>
            <form action="/translate/" enctype="multipart/form-data" method="post">
            <input name="text_field" type=str """ + f'placeholder={text}' + \
            """
            <input type="submit">
            </form>
            </body>
            """ + translation_content
    return content


def _similar_translation(en_text, text_field, en_or_dict) -> Dict[str, str]:
    """Find similar translation"""
    meaning = {}
    for words in en_or_dict.keys():
        if len(words.split()) < 2:
            # if no phrases found then no need to go further
            continue
        if {en_text}.intersection(set(words.split())):
            meaning[words] = en_or_dict[words] + "<br>"
    if meaning:
        translation = {
            "message": f"Direct translation not found for <b>{text_field}</b>. \
                         Here are few similar words: <br>",
            "english-text": text_field,
            "odia-text": f"<br> {meaning}"
        }
    return meaning and translation


@app.post("/translate/")
async def search(text_field: str = Form(...)):
    text_field = text_field.lower()
    if ud.detect_language(text_field, 0.7).get("language") == "odia":
        # Odia input text asked
        translation = _process_odia_text(text_field)
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
            translation = _similar_translation(en_text, text_field, en_or_dict)
        if not translation:
            translation = {
                "message": f"Used the <em>OpenOdia</em> library to translate <b>{text_field}</b>. <br>",
                "english-text": text_field,
                "odia-text": f"<br> {other_lang_to_odia(text_field)}"
            }
    content = _prepare_content(translation, text_field)
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
