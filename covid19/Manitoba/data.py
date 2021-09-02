# -*- coding: utf-8 -*-
"""
Data description file: data.py

@author: karlen
"""

def get_data_description():
    """ Define data provided by Esri Canada
    """
    data = {}
    data['nation'] = 'Manitoba'
    data['description'] = 'Manitoba by RHA'
    data['source'] = 'Data MB: Open Data'
    data['source_url'] = 'https://geoportal.gov.mb.ca'

    # common regional abbreviations used in the data files
    regional_abbreviations = {
        'All': 'mb',
        'Interlake-Eastern': 'ie',
        'Northern': 'no',
        'Prairie Mountain Health': 'pm',
        'Southern Health-SantÃ© Sud': 'sh',
        'Winnipeg': 'wg'
    }

    files_data = {}
    filenames = ['mb-pypm.csv','mb-vacc-pypm.csv']
    for filename in filenames:
        file_data = {}
        file_data['source'] = ''
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
        f1_populations = ['vaccinated']

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

        filename = filenames[1]
        for population in f1_populations:
            pop_data_total = {}
            pop_data_total['filename'] = filename
            header = ''
            if population == 'vaccinated':
                header = regional_abbreviations[region] + '-xt'

            pop_data_total['header'] = header

            population_data = {'total': pop_data_total}
            populations_data[population] = population_data

        regions_data[region] = populations_data

    data['regional_data'] = regions_data

    return data
