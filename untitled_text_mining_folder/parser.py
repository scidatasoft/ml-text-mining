import csv


def get_data_from_file(file_name):
    file_to_open = open(file_name, 'r', encoding='cp1251')
    lines = file_to_open.readlines()
    file_to_open.close()

    data_list = []
    data = dict()
    for index, line in enumerate(lines):
        if line.startswith('***'):
            needed_index = index + 1
            needed_line = lines[needed_index].split()
            data = fill_legand_trivial_name(needed_line)

            needed_index = index + 2
            needed_line = lines[needed_index]
            data.update(fill_legand_canonical_name(needed_line))

        if line.startswith('Metal'):
            needed_index = index + 2
            needed_line = lines[needed_index].split()
            data.update(fill_data(needed_line))
            data_list.append(data)
            data = dict()

    return data_list


def write_data_to_csv(data_list):
    csvfile_to_write = open('temp.csv', 'a')
    spamwriter = csv.writer(csvfile_to_write, delimiter='|')
    spamwriter.writerow([
        'Metal', 'Medium', 'Temp', 'Conc', 'K1', 'B2',
        'trivial_name', 'canonical_name'
    ])
    for data in data_list:
        spamwriter.writerow([
            data['metal'], data['medium'], data['temperature'],
            data['concentration'], data['k_value'], data['b_value'],
            data['legand_trivial_name'], data['legand_canonical_name']
        ])

    csvfile_to_write.close()


def fill_legand_trivial_name(needed_line):
    data = dict()
    data['legand_trivial_name'] = None
    if len(needed_line) == 6:
        data['legand_trivial_name'] = '{} {}'.format(
            needed_line[2], needed_line[3])
    elif len(needed_line) == 5:
        data['legand_trivial_name'] = needed_line[2]

    return data


def fill_legand_canonical_name(needed_line):
    data = dict()
    if ';' in needed_line:
        data['legand_canonical_name'] = needed_line.split(';')[0]
    else:
        data['legand_canonical_name'] = needed_line.rstrip()

    return data


def fill_data(needed_line):
    data = dict()
    data['metal'] = needed_line[0]
    data['medium'] = needed_line[1]
    data['temperature'] = needed_line[2]
    data['concentration'] = needed_line[3]
    data['k_value'] = needed_line[4]
    data['b_value'] = None
    if 'B2' in needed_line[5]:
        data['b_value'] = needed_line[5]

    return data


file_name = 'Fe3+.TXT'
data_list = get_data_from_file(file_name)
write_data_to_csv(data_list)
