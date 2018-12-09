import csv

from Name2InChiKey import (
    get_canonical_names_from_file, get_message, make_request
)


def convert_name(molecule):
    converted_name = molecule['canonical_name']
    converted_name = converted_name.replace(' ', '%')
    converted_name = converted_name.replace('"', '$')
    converted_name = converted_name.replace(',', '&')
    molecule['file_name'] = converted_name


def write_data_to_csv(list_of_molecules, output_csv_name):
    csvfile_to_write = open(output_csv_name, 'a', newline='')
    csv_writer = csv.writer(csvfile_to_write, delimiter=';')
    csv_writer.writerow([
        'canonical_name', 'K1', 'file_name', 'message', 'mol'
    ])
    for molecule in list_of_molecules:
        csv_writer.writerow([
            molecule['canonical_name'], molecule['K1'], molecule['file_name'],
            molecule['message'], molecule['mol']
        ])

    csvfile_to_write.close()


def write_mol_data(mol_data, mol_file_name):
    result = 'n'

    if mol_data:
        result = 'y'
        mol_data_to_write = prepare_mol_data_to_write(mol_data)

        file_to_write = open('{}.mol'.format(mol_file_name), 'w')
        file_to_write.write(mol_data_to_write)
        file_to_write.close()

    return result


def prepare_mol_data_to_write(mol_data):
    mol_data_to_write = mol_data.split('>')[0]
    mol_data_to_write = mol_data_to_write.split('\n')
    mol_data_to_write = '\n'.join(mol_data_to_write[3:])
    mol_data_to_write = mol_data_to_write.replace('\r', '')

    return mol_data_to_write


if __name__ == '__main__':
    print('Process input file')
    input_csv = 'start.csv'
    list_of_molecules = get_canonical_names_from_file(input_csv)

    print('Get data from chem spider')
    for molecule in list_of_molecules:
        print('Process molecule: {}'.format(molecule['canonical_name']))
        convert_name(molecule)
        response_as_dict = make_request(molecule)
        mol_result = write_mol_data(
            response_as_dict['mol'], molecule['file_name'])
        molecule['message'] = get_message(response_as_dict['message'])
        molecule['mol'] = mol_result

    print('Write data to csv')
    output_csv = 'finish.csv'
    write_data_to_csv(list_of_molecules, output_csv)
