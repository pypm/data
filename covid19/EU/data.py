# -*- coding: utf-8 -*-
"""
Example of data description file: data.py

@author: karlen
"""

def get_data_description():
    """ Define data
    """
    data = {}
    data['nation'] = 'EU'
    data['description'] = 'EU by State'
    data['source'] = 'JHU'
    data['source_url'] = 'https://github.com/epiforecasts/covid19-forecast-hub-europe/tree/main/data-truth/JHU'

    # common regional abbreviations used in the data files
    regional_abbreviations = {
        'Austria': 'AT',
        'Belgium': 'BE',
        'Bulgaria': 'BG',
        'Croatia': 'HR',
        'Cyprus': 'CY',
        'Czechia': 'CZ',
        'Denmark': 'DK',
        'Estonia': 'EE',
        'Finland': 'FI',
        'France': 'FR',
        'Germany': 'DE',
        'Greece': 'GR',
        'Hungary': 'HU',
        'Iceland': 'IS',
        'Ireland': 'IE',
        'Italy': 'IT',
        'Latvia': 'LV',
        'Liechtenstein': 'LI',
        'Lithuania': 'LT',
        'Luxembourg': 'LU',
        'Malta': 'MT',
        'Netherlands': 'NL',
        'Norway': 'NO',
        'Poland': 'PL',
        'Portugal': 'PT',
        'Romania': 'RO',
        'Slovakia': 'SK',
        'Slovenia': 'SI',
        'Spain': 'ES',
        'Sweden': 'SE',
        'Switzerland': 'CH',
        'United Kingdom': 'GB'
    }

    files_data = {}
    filenames = ['eu-jhu-pypm.csv']
    sources = ['JHU']
    for i,filename in enumerate(filenames):
        file_data = {}
        file_data['source'] = sources[i]
        file_data['date header'] = 'Date'
        file_data['date start'] = [2020, 3, 1]

        files_data[filename] = file_data
    data['files'] = files_data

    #for each region, define location of each population data (file/column header)
    #either daily or total (or both) data can be provided

    regions_data = {}
    f0_populations = ['reported', 'deaths']

    for region in regional_abbreviations:

        populations_data = {}

        filename = filenames[0]
        for population in f0_populations:
            pop_data_total = {}
            pop_data_total['filename'] = filename
            header = ''
            if population == 'reported':
                header = regional_abbreviations[region]+'-pt'
            if population == 'deaths':
                header = regional_abbreviations[region]+'-dt'

            pop_data_total['header'] = header

            population_data = {'total': pop_data_total}
            populations_data[population] = population_data

        regions_data[region] = populations_data

    data['regional_data'] = regions_data

    return data
