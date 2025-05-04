from flask import Flask, render_template, request, redirect, url_for, jsonify
from google.genai import types
from google import genai

from dotenv import load_dotenv
from dotenv import dotenv_values

import os

load_dotenv()

config = {
  **dotenv_values(".env"), # environnement
  **os.environ,            # override loaded values with environment variables
}


API=config.get('API')
NAME=config.get('NAME') or "gemmAI"

app = Flask(NAME)





class info:
   name:str = app.name
   version:str = "0.0.2"
   year:int = 2025

app.jinja_env.globals['info']=info()


@app.route('/')
def index():
    return render_template('index.html')

class resp():
    text:str = "Response"


@app.route("/chat",methods=['GET','POST'])
def chat():
    info=request.get_json()
    model="gemini-2.0-flash"
    client=genai.Client(api_key=API)
    if 'previous' in info:
       system_instruction=info['previous']
    else:
       system_instruction="""tu es un chat bot francophone,
            fait une réponse dans un style cordiale.
            n'ajoute pas de décoration autour de la réponse, et pas de message d'avis.
            supprime "n'hésitez pas si vous avez d'autres questions".
            supprime les messages de conclusion et d'opinion sur la réponse.
            cite les sources.
            """
    config=types.GenerateContentConfig(
          system_instruction= system_instruction)

    content=info['text']
    response= client.models.generate_content(
            model=model,
            config=config,
            contents=content)

    data={'status': 'ok', 'msg': response.text }

    return jsonify(data)





if __name__ == "__main__":
   app.run(debug=True,host="0.0.0.0",port="5000")
