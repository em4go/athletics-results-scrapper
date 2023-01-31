import json
from process import *

# paths = [
#     'regional_puertollano.pdf',
#     'gp-valencia.pdf',
#     'provincial_absoluto_elche.pdf'
# ]

# for path in paths:

#     results = get_results(path)
#     dump_name = path + '.json'
#     with open(dump_name, 'w', encoding='utf-8') as json_file:
#         json.dump(results, json_file, ensure_ascii=False, indent=4)

path = 'control_albacete.pdf'
results = get_results(path, indoor=False)
# i = 0
# while i < len(results):
#     race = results[i]
#     if len(race['athletes']) == 0:
#         del results[i]
#     else:
#         i += 1
dump_name = path + '.json'
with open(dump_name, 'w', encoding='utf-8') as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)

# categories = {
#     '0': 'Absoluto',
#     '1': 'Sub-16',
#     '2': 'Sub-18',
#     '3': 'Sub-20',
#     '4': 'Sub-23',
# }
# n_pdf = int(input('De cuántos archivos quieres obtener los atletas?\n'))
# paths_list = {}
# for i in range(n_pdf):
#     name = input(
#         f'Introduce el nombre del PDF número {i} (Recuerda incluir la extensión. Ej: "Antequera220123.pdf"):\n')
#     category_code = input(f'''Introduce el número correspondiente a la categoría del campeonato o control {name}:
#     - (0 o 'Enter') -> Absoluto
#     - (1) -> Sub-16
#     - (2) -> Sub-18
#     - (3) -> Sub-20
#     - (4) -> Sub-23
#     ''')
#     category = categories.get(category_code, 'Absoluto')
#     paths_list[name] = category

# for path, category in paths_list.items():
#     results = get_results(path, category)
#     dump_name = path + '.json'
#     with open(dump_name, 'w', encoding='utf-8') as json_file:
#         json.dump(results, json_file, ensure_ascii=False, indent=4)
