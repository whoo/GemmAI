# Gem-AI

Ce projet explore la création d'une application web de chatbot.
Il utilise l'API Google Gemini pour générer des réponses et s'appuie sur un backend en Python Flask et un frontend en JavaScript pour l'interaction utilisateur.
L'objectif principal de cette expérimentation est de comprendre comment intégrer et exploiter les capacités de l'API Google Gemini dans une application web simple.


# Démarrage

## Mise à jour .env

* api key de google API="..."
* nom de l'application NAME="..."

L'api key pour google se génére facilement dans l'[aistudio](https://aistudio.google.com/apikey)

## Lancement


### Shell 
```bash
python3 -m venv venv
. venv/bin/activate
pip install -r GemmAI/requirements.txt
cd GemmAI
flask run --debug -h 0.0.0.0

```

### Docker

```bash
NAME="gemmai"
API="..."
docker built -t $NAME .
docker run -d -n $NAME -env API=$API -p XXXX:8090 $NAME

```


