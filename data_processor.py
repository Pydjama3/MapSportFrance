import csv

import pygal
from pygal.style import Style

# MAIN_DATA = "data/licencies.csv" #https://www.pygal.org/en/3.0.0/documentation/custom_styles.html

# NAME_TOT = "Total"
# NAME_DEPARTEMENT = "Département"


def load_csv_file(file_name: str, name_department: str,
                  name_value: str) -> dict[int, int | float]:
    data = {}
    with open(file_name) as opened_file:
        csv_reader = csv.reader(opened_file, delimiter=';')

        pos_value: int
        pos_department: int

        lines = 0
        for row in csv_reader:
            if lines == 0:
                pos_value = row.index(name_value)
                pos_department = row.index(name_department)
            else:
                if row[pos_department] not in data:
                    data[row[pos_department]] = float(row[pos_value])
                else:
                    data[row[pos_department]] += float(row[pos_value])
            lines += 1
        return data


def compute_data(data: dict, formula=lambda x: x) -> dict[int, int | float]:
    for department in data:
        data[department] = formula(data[department])
    return data


def cross_compute_data(data: dict,
                       expressions: dict[int, str]) -> dict[int, int | float]:
    generated_data = {}
    departments = set()
    for departments_list_index in data:
        if len(departments) == 0:
            departments = set(data[departments_list_index])
        else:
            departments.intersection_update(set(data[departments_list_index]))
    for department in departments:
        V = {}
        for id in data:
            V[id] = data[id][department]
        for id in data:
            if id not in generated_data:
                generated_data[id] = {}
            generated_data[id][department] = eval(expressions[id]) if len(
                expressions[id]) > 0 else data[id][department]
    return generated_data


def generate_plots(globalTitle: str, plots: dict) -> None:
    print("--- DATA MAP VISUALIZATION ---")

    print("\t- Retrieving data...")
    raw_data = {}
    formulas = {}
    graph_colors = []
    for id in plots:
        raw_data[id] = load_csv_file("data/" + plots[id]["file"],
                                     plots[id]["departments"],
                                     plots[id]["values"])
        formulas[id] = plots[id]["formula"]
        if "display" in plots[id]:
            graph_colors.append(plots[id]["color"])
    print("\t\t=> Data retrieved")

    print("\t- Initializing map...")
    custom_style = Style(colors=graph_colors)
    fr_chart = pygal.maps.fr.Departments(human_readable=True,
                                         style=custom_style)
    fr_chart.title = globalTitle
    print("\t\t=> Map initialized")

    print("\t- Computing data...")
    computed_data = cross_compute_data(raw_data, formulas)
    print("\t\t=> Data computed")

    print("\t- Adding data to map...")
    count = 0
    for id in computed_data:
        if "display" not in plots[id]:
            print(plots[id])
            continue

        print(id, plots[id]["title"], computed_data[id])
        fr_chart.add(plots[id]["title"], computed_data[id])
        count += 1
    print(f"\t\t=> {count} data set(s) added to map")

    print("\t- Generating HTML...")
    fr_chart.render_to_file('templates/index.html')
    print("\t\t=> HTML generated")

    print("--- TASK FINISHED ---")
