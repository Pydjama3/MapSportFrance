import random

from flask import Flask, render_template, request

from data_processor import generate_plots

app = Flask(  # Créer un flask app
    __name__,
    template_folder='templates',  # Nom du fichier avec les pages html
    static_folder='static'  # Nom du dossier avec les fichiers "statics"
)

@app.route('/carte',  methods=['POST'])  # '/' pour la page par défault
def carte():
    globalTitle = ""
    plots = {}
    for key, value in request.form.items():
        if key == "globalTitle":
            globalTitle = value
        else:
            id, plot_property = key[5:].split("][")
            id = int(id[1:])
            plot_property = plot_property[:len(plot_property)-1]
            if id not in plots:
                plots[id] = {plot_property: value}
            else:
                plots[id][plot_property] = value
    print(plots)
    generate_plots(globalTitle, plots)
    return render_template('index.html')


@app.route('/')  # '/' pour la page par défault
def home():
  return render_template('homepage.html')

@app.route('/carte_test')
def test():
    return render_template('index.html')


app.run(host='0.0.0.0', port=80) # random.randint(2000, 9000))
