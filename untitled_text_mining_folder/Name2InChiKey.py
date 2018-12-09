import csv
import json
import urllib.request

from urllib.parse import urlencode


def get_canonical_names_from_file(file_name):
    file_to_read = open(file_name, 'r')
    csv_file = csv.reader(file_to_read, delimiter=';')

    list_of_molecules = []

    first_line = True
    for row in csv_file:
        if first_line:
            first_line = False
            continue

        canonical_name = row[0]
        k_value = row[1]
        data_dict = {
            'canonical_name': canonical_name,
            'K1': k_value
        }
        list_of_molecules.append(data_dict)

    file_to_read.close()

    return list_of_molecules


def make_request(molecule):
    query_string = make_query_string(molecule['canonical_name'])
    response_body = urllib.request.urlopen(query_string).read().decode()
    response_as_dict = json.loads(response_body)

    return response_as_dict


def write_data_to_csv(list_of_molecules, output_csv_name):
    csvfile_to_write = open(output_csv_name, 'a', newline='')
    csv_writer = csv.writer(csvfile_to_write, delimiter=';')
    csv_writer.writerow(['canonical_name', 'K1', 'message', 'inchikey'])
    for molecule in list_of_molecules:
        csv_writer.writerow([
            molecule['canonical_name'], molecule['K1'],
            molecule['message'], molecule['inchikey']
        ])

    csvfile_to_write.close()


def make_query_string(canonical_name):
    base = 'http://parts.chemspider.com/JSON.ashx'

    parameters = {
        'op': 'ConvertTo',
        'convertOptions.Text': canonical_name,
        'convertOptions.Direction': 'Name2Mol'
    }
    encoded_parameters = urlencode(parameters)
    query_string = '{}?{}'.format(base, encoded_parameters)

    return query_string


def get_inchikey(mol_data):
    std_inchi_key = 'n'

    if mol_data:
        for value in mol_data.split('<'):
            if 'StdInChIKey' in value:
                std_inchi_key = value.split('>')[1]
                std_inchi_key = std_inchi_key.replace('\r', '')
                std_inchi_key = std_inchi_key.replace('\n', '')
                std_inchi_key = std_inchi_key.rstrip()
                break

    return std_inchi_key


def get_message(message):
    if not message:
        return 'n'

    return message


if __name__ == '__main__':
    print('Process input file')
    input_csv = 'start.csv'
    list_of_molecules = get_canonical_names_from_file(input_csv)

    print('Get data from chem spider')
    for molecule in list_of_molecules:
        print('Get data for molecule: {}'.format(molecule['canonical_name']))
        response_as_dict = make_request(molecule)
        molecule['message'] = get_message(response_as_dict['message'])
        molecule['inchikey'] = get_inchikey(response_as_dict['mol'])

    print('Write data to csv')
    output_csv = 'inchi.csv'
    write_data_to_csv(list_of_molecules, output_csv)
