# -*- coding: utf-8 -*-
"""
Example of data description file: data.py

@author: karlen
"""


def get_data_description():
    """ Define data provided by W. Cota
    """
    data = {}
    data['nation'] = 'Brazil'
    data['description'] = 'Brazil by state'
    data['source'] = 'Collection from W. Cota using official information given by Ministério da Saúde'
    data['source_url'] = 'https://doi.org/10.1590/SciELOPreprints.362 and https://github.com/wcota/covid19br'

    # common regional abbreviations used in the data files
    regional_abbreviations = {
        'AC: Acre': 'AC',
        'AL: Alagoas': 'AL',
        'AP: Amapá': 'AP',
        'AM: Amazonas': 'AM',
        'BA: Bahia': 'BA',
        'CE: Ceará': 'CE',
        'DF: Distrito Federal': 'DF',
        'ES: Espírito Santo': 'ES',
        'GO: Goiás': 'GO',
        'MA: Maranhão': 'MA',
        'MT: Mato Grosso': 'MT',
        'MS: Mato Grosso do Sul': 'MS',
        'MG: Minas Gerais': 'MG',
        'PA: Pará': 'PA',
        'PB: Paraíba': 'PB',
        'PR: Paraná': 'PR',
        'PE: Pernambuco': 'PE',
        'PI: Piauí': 'PI',
        'RJ: Rio de Janeiro': 'RJ',
        'RN: Rio Grande do Norte': 'RN',
        'RS: Rio Grande do Sul': 'RS',
        'RO: Rondônia': 'RO',
        'RR: Roraima': 'RR',
        'SC: Santa Catarina': 'SC',
        'SP: São Paulo': 'SP',
        'SE: Sergipe': 'SE',
        'TO: Tocantins': 'TO'
    }

    files_data = {}
    filenames = ['brazil-pypm.csv']
    for filename in filenames:
        file_data = {}
        file_data['source'] = 'More detailed information if folder has multiple sources'
        file_data['date header'] = 'Date'
        file_data['date start'] = [2020, 3, 1]

        files_data[filename] = file_data
    data['files'] = files_data

    # for each region, define location of each population data (file/column header)
    # either daily or total (or both) data can be provided

    regions_data = {}
    for region in regional_abbreviations:

        populations_data = {}

        f0_populations = ['reported', 'deaths']
        filename = filenames[0]
        for population in f0_populations:
            pop_data_total = {}
            pop_data_total['filename'] = filename
            header = ''
            if population == 'reported':
                header = regional_abbreviations[region] + '-pt'
            if population == 'deaths':
                header = regional_abbreviations[region] + '-dt'

            pop_data_total['header'] = header

            population_data = {'total': pop_data_total}
            populations_data[population] = population_data

        regions_data[region] = populations_data

    data['regional_data'] = regions_data

    return data
