import json
from process import get_results

path = 'gp-valencia.pdf'
results = get_results(path, indoor=False)
# Para elminiar las pruebas en las que no hay atletas
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


#-----------------------------------------------------------------------------
# Ejemplo de programa para utilizar muchos archivos de una vez
# n_pdf = int(input('De cuántos archivos quieres obtener los atletas?\n'))
# paths_list = []
# for i in range(n_pdf):
#     name = input(
#         f'Introduce el nombre del PDF número {i} (Recuerda incluir la extensión. Ej: "Antequera220123.pdf"):\n')
    # indoor = input('Es una competición de pista cubierta? (S/N)\n')
    # if 's' in indoor.lower():
    #     pc = True
    # else:
    #     pc = False
#     paths_list.append(name)

# for path in paths_list:
#     results = get_results(path, pc)
#     dump_name = path + '.json'
#     with open(dump_name, 'w', encoding='utf-8') as json_file:
#         json.dump(results, json_file, ensure_ascii=False, indent=4)
