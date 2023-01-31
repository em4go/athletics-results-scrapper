import pdfplumber
import re
import regex

categories = {
    'SUB16': 'Sub-16',
    'SUB18': 'Sub-18',
    'SUB20': 'Sub-20',
    'SUB23': 'Sub-23',
    'ABSOLUTO': 'Absoluto'
}


# def get_category(line, default):
#     category = re.search(regex.category, line)
#     if category is None:
#         return default
#     return categories.get(category, category)

def get_athlete_category(year):
    correspondence = {
        '2001': 'Sub-23',
        '2002': 'Sub-23',
        '2003': 'Sub-23',
        '2004': 'Sub-20',
        '2005': 'Sub-20',
        '2006': 'Sub-18',
        '2007': 'Sub-18',
        '2008': 'Sub-16',
        '2009': 'Sub-16',
        '2010': 'Sub-14',
        '2011': 'Sub-14',
    }
    return correspondence.get(year, 'Absoluto')

def delete_duplicated(file):
    return_text = ''
    for line in file:
        if line not in return_text:
            return_text += line
    return return_text


def pdf_to_txt(path):
    try:
        with pdfplumber.open(path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() + '\n'
            return text
    except:
        print('Couldn\'t open the pdf file')
        return None


def scrap_line(line):
    date = re.search(regex.date, line)
    marks = re.findall(regex.mark, line)
    name = re.search(regex.complete_name, line)
    if (' NP ' in line) or (' AB ' in line) or (' DS ' in line) or (' SM ' in line) or (date is None) or (len(marks) == 0) or (name is None):
        return None
    a = {}
    a["name"] = name.group()
    birthday = date.group()
    a["birthday"] = birthday
    year = birthday.split('/')[-1]
    category = get_athlete_category(year)
    a["category"] = category
    a["mark"] = max(marks)
    return a


# def get_text(path):
#     with open(path, encoding='utf-8') as txt:
#         text = txt.readlines()
#     return text


def get_event(line):
    line_list = line.split()

    # Tipo de carrera
    if 'VALLAS' in line.upper() or 'TRIPLE' in line.upper():
        race_name = ' '.join(line_list[:2])
    else:
        race_name = line_list[0]

    return race_name


def correct_duplicated_letters(line):
    corrected_line = ''
    for i in range(len(line)):
        char = line[i]
        if i % 2 == 0:
            corrected_line += char
    return corrected_line


def get_results(pdf_path, indoor=False):
    text = pdf_to_txt(pdf_path)
    if text is not None:
        text = text.split('\n')

        results = []
        races_order = {}
        i = 0
        for index, line in enumerate(text):
            upper_line = line.upper()
            if 'FEM' in line or 'MASC' in line or 'MMAASSCC' in line or 'FFEEMM' in line or 'HOMBRES' in upper_line or 'MUJERES' in upper_line:
                if 'MMAASSCC' in line or 'FFEEMM' in line:
                    line = correct_duplicated_letters(line)
                actual_race = line.strip()

                # Categoría de la carrera
                # category = get_category(line, default_category)

                # Type of event
                race_name = get_event(line)

                # Carrera masculina o femenina
                if 'F' in line or 'J' in upper_line:
                    genre = 'female'
                else:
                    genre = 'male'

                # Add race to the list
                if actual_race not in races_order:
                    races_order[actual_race] = i
                    event = {
                        'name': race_name,
                        'genre': genre,
                        'indoor': indoor,
                        'athletes': []
                    }
                    results.append(event)
                    i += 1

            athlete = scrap_line(line)
            if athlete is not None:
                race_index = races_order[actual_race]
                next_line = text[index+1]
                licens = re.search(regex.licens, next_line)
                if licens is not None:
                    athlete["license"] = licens.group()
                results[race_index]['athletes'].append(athlete)
        return results


if __name__ == '__main__':
    path = 'gp-valencia.pdf'
    out_txt = path + '.txt'
    pdf_to_txt(path, out_txt)
    # with open(out_txt, encoding='utf-8') as txt:
    #     print(delete_duplicated(txt))

"""
(Posición) - Dorsal - [Nombre y Apellidos] - [Fecha de nacimiento] - Calle - [Marca] - Q?
athlete = {
    name: "Ernesto Martínez Gómez",
    birthday: "27/05/2004",
    mark: "50.61"
    license: "AB13"
    (e): False
}

race = {
    name: '60m MASC.',
    athletes: [
        a1,
        a2,
        a3
    ]
}

results = [
    r1,
    r2,
    r3
]

"""
