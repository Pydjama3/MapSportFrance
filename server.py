import random

from flask import Flask, render_template

app = Flask(  # Créer un flask app
    __name__,
    template_folder='templates',  # Nom du fichier avec les pages html
    static_folder='static'  # Nom du dossier avec les fichiers "statics"
)

@app.route('/carte')  # '/' pour la page par défault
def carte():
  return render_template('index.html', )


@app.route('/')  # '/' pour la page par défault
def home():
  return render_template('homepage.html', )


app.run(host='0.0.0.0', port=random.randint(2000, 9000))
