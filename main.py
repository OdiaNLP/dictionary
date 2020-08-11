import json

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()
with open("./data/structured_wordlist.json", "r") as fh:
    word_dict = json.load(fh)


@app.post("/translate/")
async def search(text_field: str = Form(...)):
    if text_field in word_dict:
        return {
            "text_field": text_field,
            "meaning": word_dict[text_field]["word_details"]
        }
    else:
        return {
            "message": "The word is not found in the corpus."
        }


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
