from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import flask_login

from google.genai import types
from google import genai

from dotenv import load_dotenv
from dotenv import dotenv_values

from forms import *
import os

import uuid

from werkzeug.security import check_password_hash,generate_password_hash

load_dotenv()

config = {
  **dotenv_values(".env"), # environnement
  **os.environ,            # override loaded values with environment variables
}


API=config.get('API')
NAME=config.get('NAME') or "gemmAI"

app = Flask(NAME)

app.config['WTF_CSRF_SECRET_KEY']= "superRandomString"
app.config['SECRET_KEY']="generateSecret"

basedir=os.path.abspath(os.path.dirname(__file__))
dbfile ="/../db/user.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{basedir}{dbfile}'
print(app.config['SQLALCHEMY_DATABASE_URI'])

from models import *

db = SQLAlchemy(model_class=Base)
migrate = Migrate(app, db)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view="/login"

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    user=User.query.get(user_id)
    app.logger.info(user)
    return user



class info:
   name:str = app.name
   version:str = "0.0.3"
   year:int = 2025

app.jinja_env.globals['info']=info()


@app.route('/')
def index():
    return render_template('index.html')

class resp():
    text:str = "Response"

@app.route("/login",methods=['GET','POST'])
def login():

    form=LoginForm()
    if form.validate_on_submit():
        username = form.name.data
        # u=load_user(username)
        u=User.query.filter(User.username==username).first()
        if u is not None:
           upass = form.password.data
           if check_password_hash( u.password , upass):
              flask_login.login_user(u)
              flash('Logged in successfully.',"success")
           else:
              flash("Erreur de connexion","warning")
    
        else:
           flash("Erreur de login","danger")
        return redirect(url_for('index'))

    return render_template("login.html",form=form)

@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect("/")


@app.route("/chat",methods=['POST'])
@flask_login.login_required
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
