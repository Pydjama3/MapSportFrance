import csv
from types import LambdaType

# import pandas as pd
import pygal
from PIL import Image
from pygal import style
from pygal.style import Style

MAIN_DATA = "data/main_src.csv" #https://www.pygal.org/en/3.0.0/documentation/custom_styles.html

NAME_TOT = "Total"
NAME_DEPARTEMENT = "Département"


def load_csv_file(file_name: str, name_department: str, name_value: str) -> dict[int, int | float]:
    data = {}
    with open(file_name) as opened_file:
        csv_reader = csv.reader(opened_file, delimiter=';')
        print("\t\t=> Data received")

        print("\t- Formatting data...")
        pos_value = None
        pos_department = None

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

def compute_data(data: dict, formula = lambda x:x) -> dict[int, int | float]:
  for department in data:
    data[department] = formula(data[department])

  return data
    


if __name__ == "__main__":
    print("--- DATA MAP VISUALIZATION ---")

    print("\t- Initializing map...")
    custom_style = Style(background='transparent',
         plot_background='transparent',
         foreground='#53E89B',
         foreground_strong='#53A0E8',
         foreground_subtle='#630C0D',
         opacity='.6',
         opacity_hover='.9',
         transition='400ms ease-in',
         colors=('#E853A0', '#E8537A', '#E95355', '#E87653',
                 '#E89B53'))
    fr_chart = pygal.maps.fr.Departments(human_readable=True, style=custom_style)
    fr_chart.title = 'Licenciés par départment'
    print("\t\t=> Map initialized")

    print("\t- Requesting data...")
    raw_data = load_csv_file(MAIN_DATA, NAME_DEPARTEMENT, NAME_TOT)
    data = compute_data(raw_data)
    print("\t\t=> Data formatted")

    print("\t- Adding data to map...")
    fr_chart.add('In 2021', data)
    print("\t\t=> Data added to map")

    print("\t- Generating HTML...")
    fr_chart.render_to_file('templates/index.html')
    print("\t\t=> HTML generated")

    print("--- TASK FINISHED ---")
