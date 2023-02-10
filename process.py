import pdfplumber
import re
import regex

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


def pdf_to_txt_file(path):
    try:
        with pdfplumber.open(path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() + '\n'
            with open(path + '.txt', 'w') as file:
                file.write(text)
            return text
    except:
        print('Couldn\'t open the pdf file')
        return None
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


def scrap_line(line, combi = False):
    date = re.search(regex.date, line)
    marks = []
    if combi:
        marks = re.findall(regex.combi_mark, line)
    else:
        marks = re.findall(regex.mark, line)
    name = re.search(regex.complete_name, line)
    if not combi:
        if ('RE ' in line) or ('RC ' in line) or (' NP ' in line) or (' AB ' in line) or (' DS ' in line) or (' SM ' in line) or (date is None) or (len(marks) == 0) or (name is None):
            return None
    else: 
        if (date is None) or (len(marks) == 0) or (name is None):
            return None
    a = {}
    a["name"] = name.group()
    birthday = date.group()
    a["birthday"] = birthday
    year = birthday.split('/')[-1]
    category = get_athlete_category(year)
    a["category"] = category
    if combi:
        mark = marks[-1]
    else:
        mark = max(marks)
    a["mark"] = mark
    return a


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
    actual_iteration = line
    while not ('MASC' in corrected_line or 'HOM' in corrected_line.upper() or 'FEM' in corrected_line or 'MUJ' in corrected_line.upper()):
        corrected_line = ''
        for i in range(len(actual_iteration)):
            char = actual_iteration[i]
            if i % 2 == 0:
                corrected_line += char
        actual_iteration = corrected_line
    return corrected_line


def get_results(pdf_path, indoor=False, location='', date=''):
    text = pdf_to_txt(pdf_path)
    if text is not None:
        text.replace(' ', ' ')
        text.replace('‐', '-')
        text = text.split('\n')

        results = []
        races_order = {}
        i = 0
        combi = False
        genre = 'male'
        race_name = ''
        actual_race = ''
        for index, line in enumerate(text):
            upper_line = line.upper()
            if 'FEM' in line or 'MASC' in line or 'MMA' in line or 'FFE' in line or 'HOMBRES' in upper_line or 'MUJERES' in upper_line or 'TLÓN' in upper_line:
                if 'MM' in line or 'FF' in line or 'HH' in line:
                    line = correct_duplicated_letters(line)
                    upper_line = correct_duplicated_letters(upper_line)
                if 'TLÓN' not in upper_line:
                    combi = False
                else:
                    combi = True
                if not ('FEM' in line or 'MASC' in line or 'HOMBRES' in upper_line or 'MUJERES' in upper_line):
                    combi = False
                actual_race = line.strip()

                # Type of event
                race_name = get_event(line)

                # Male or female event
                if 'F' in line or 'J' in upper_line:
                    genre = 'female'
                elif 'SC' in line or 'HOM' in upper_line:
                    genre = 'male'
                

                # Add race to the list
                if actual_race not in races_order:
                    races_order[actual_race] = i
                    event = {
                        'name': race_name,
                        'genre': genre,
                        'indoor': indoor,
                        'location': location,
                        'date': date,
                        'wind': 0,
                        'athletes': []
                    }
                    results.append(event)
                    i += 1
                continue
            athlete = scrap_line(line, combi)
            if 'Salvador' in line:
                print(athlete)
            if athlete is not None:
                race_index = races_order[actual_race]
                next_line = text[index+1]
                licens = re.search(regex.licens, next_line)
                if licens is not None:
                    athlete["license"] = licens.group()
                results[race_index]['athletes'].append(athlete)
        return results


def get_decathlon(pdf_path, indoor=False):
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

                # Type of event
                race_name = get_event(line)

                # Male or female event
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
                        'wind': 0,
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