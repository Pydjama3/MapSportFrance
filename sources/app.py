import random

from data_processor import generate_plots
from flask import Flask, render_template, request

app = Flask(  # Créer une application Flask
    __name__,
    template_folder='templates',  # Nom du fichier avec les pages html
    static_folder='static'  # Nom du dossier avec les fichiers "statics"
)


@app.route('/carte', methods=['POST'])
def carte():
    """
    Affichage de la carte principale en suivant la requête
    de l'utilisateur ("POST")
    """
    # Récupération des données de l'utilisateur et parsing
    globalTitle = ""
    plots = {}
    for key, value in request.form.items():
        if key == "globalTitle":
            globalTitle = value
        else:
            id, plot_property = key[5:].split("][")
            id = int(id[1:])
            plot_property = plot_property[:len(plot_property) - 1]
            if id not in plots:
                plots[id] = {plot_property: value}
            else:
                plots[id][plot_property] = value

    # Génération de la carte (importé depuis data_processor.py)
    generate_plots(globalTitle, plots)

    return render_template('index.html', globalTitle=globalTitle)


@app.route('/')  # '/' pour la page par défault
def home():
    return render_template('homepage.html')


@app.route(
    '/carte_test')  # pour vérifier les résultats sans passer par le formulaire
def test():
    return render_template('index.html')


app.run(host='0.0.0.0', port=80,
        debug=True)  # debug=True pour afficher les erreurs
