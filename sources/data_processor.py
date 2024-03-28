import csv

import pygal
from pygal.style import Style

BASE_DATA_DIR_PATH = "data/"


def load_csv_file(file_name: str, name_department: str,
                  name_value: str) -> dict[int, int | float]:
    """
    Receuillir les données d'un fichier csv et les stocker dans un dictionnaire

    Paramètres:
        file_name: chemin/nom du fichier csv
        nane_department: nom de la colonne contenant les codes des départements
        naem_value: nom de la colonne contenant les valeurs

    Retourne:
        dictionnaire des valeurs (de la forme {<code département>: <valeur>})
    """
    data = {}
    try:
        with open(file_name) as opened_file:  #ouverture du fichier
            # lecture du fichier et mise en forme dans un tableau
            csv_reader = csv.reader(opened_file, delimiter=';')

            pos_value = -1
            pos_department = -1

            lines = 0
            for row in csv_reader:
                if lines == 0:
                    # index des colonnes (...des valeurs, ... des départements)
                    pos_value = row.index(name_value)
                    pos_department = row.index(name_department)
                else:
                    if row[pos_department] not in data:
                        data[row[pos_department]] = float(row[pos_value])
                    else:
                        data[row[pos_department]] += float(row[pos_value])
                lines += 1
    except:
        raise
    return data


def compute_data(data: dict, formula=lambda x: x) -> dict[int, int | float]:
    """
    Appliquer une formule sur un jeu de données

    Paramètres:
        data: dictionnaire des valeurs initiales (de la 
              forme {<code département>: <valeur>})
        fomula: fonction à appliquer sur les valeurs

    Retourne:
        un dictionnaire des valeurs calculées (de la forme {<code département>: <valeur>})
    """
    for department in data:
        data[department] = formula(data[department])
    return data


def cross_compute_data(data: dict,
                       expressions: dict[int, str]) -> dict[int, int | float]:
    """
    Applique des formules à travers plusieurs jeux de données

    Paramètres:
        data: dictionnaire des valeurs sources (de la 
            forme {<id des données>: <données>})
        expessions: dictionnaire des formules à appliquer sur les valeurs
            sources (de la forme {<id des données>: <formule>})

    Retourne:
        un dictionnaire des valeurs calculées 
            (de la forme {<id des données>: <données calculées>})
    """

    # on établit une liste des départements dont on peut calculer les valeurs
    # (choix d'un <set>: la fonction "intersection_update")
    generated_data = {}
    departments = set()
    for departments_list_index in data:
        if len(departments) == 0:
            departments = set(data[departments_list_index])
        else:
            departments.intersection_update(set(data[departments_list_index]))

    # dans l'ordre des département, on calcule les valeurs pour chaque formules
    for department in departments:
        # on met les données dans un dictionnaire pour
        # pouvoir les utiliser dans la formule
        # (plut simple pour l'utilisateur de taper "V[n]")
        V = {}
        for source_id in data:
            V[source_id] = data[source_id][department]

        # on calcule la valeur en évaluant la formule
        # (*pas très sécurisé, mais ça marche ^_^*)
        for id in expressions:
            if id not in generated_data:
                generated_data[id] = {}
            generated_data[id][department] = eval(expressions[id]) if len(
                expressions[id]) > 0 else None
    return generated_data


def generate_plots(globalTitle: str, plots: dict) -> None:
    """
    Générer les graphiques à partir d'un requête de l'utilisateur.
    C'est la partie centrale du code, elle emploie la plupart des fonctions
    implémentées.
    Les logs permettent de suivre l'avancement de la tâche.

    Paramètres:
        globalTitle: titre global de la carte
        plots: dictionnaire des plots à générer 
            (de la forme {<id des données>: <contenu de la requête>})

    Retourne:
        Rien, un fichier (index.html) est généré dans le dossier "static"

    Note:
        Fonction appelée par app.route('/carte')
    """
    print("--- DATA MAP VISUALIZATION ---")

    if len(plots) < 1:
        raise ValueError("No plots to generate")

    # on récupère tout
    print("\t- Retrieving data...")
    raw_values_of = {}
    calculate_values_for = {}
    to_plot = []
    done = 0
    errors = 0
    for plot_id in plots:
        # on récupère les données des fichiers renseignés
        if plots[plot_id]["type"] == "file":
            try:
                raw_values_of[plot_id] = load_csv_file(
                    BASE_DATA_DIR_PATH + plots[plot_id]["file"],
                    plots[plot_id]["departments"], plots[plot_id]["values"])
            except:
                print(
                    f"\t\t- Error while loading file {plots[plot_id]['file']}")
                errors += 1
            else:
                done += 1
        # on "isole" les éléments dont on devra calculés des valeurs pour plus tard...
        else:
            calculate_values_for[plot_id] = plots[plot_id]["formula"]

        # on fait un liste des données à afficher
        if "display" in plots[plot_id]:
            to_plot.append(plot_id)

    print("\t\t=> Data retrieved from " + str(done) + " files (" +
          str(errors) + " errors)")

    print("\t- Computing data...")
    try:
        # on calcule les données
        computed_data = cross_compute_data(raw_values_of, calculate_values_for)
    except:
        print("=> No data was computed or calculated...")
        raise
    else:
        print("\t\t=> Data computed")

    print("\t- Initializing map...")
    # on initialise la carte pour y ajouter les données après
    fr_chart = pygal.maps.fr.Departments(human_readable=True)
    fr_chart.title = globalTitle
    print("\t\t=> Map initialized")

    print("\t- Adding data to map...")
    # on affiche ce qu'il faut en récupurant les données des bon dictionnaires
    done = 0
    errors = 0
    colors = []
    for id in to_plot:
        try:
            if id in computed_data:
                fr_chart.add(plots[id]["title"], computed_data[id])
            else:
                fr_chart.add(plots[id]["title"], raw_values_of[id])
            colors.append(plots[id]["color"])
        except:
            print(
                f"\t\t- Error while adding data to map for {plots[id]['title']}"
            )
            errors += 1
            raise
        else:
            done += 1
    print(f"\t\t=> {done} data set(s) added to map (errors: {errors})")

    print("\t- Generating HTML...")
    # on rajoute du *style* à la carte en prenant en compte les couleurs
    # choisies par l'utilisateur
    custom_style = Style(colors=colors)
    fr_chart.style = custom_style
    fr_chart.render_to_file('templates/index.html')
    print("\t\t=> HTML generated")

    # FIN DU CODE --- tada!
    print("--- TASK FINISHED ---")
