# -*- coding: utf-8 -*-
"""
Example of data description file: data.py

@author: karlen
"""

def get_data_description():
    """ Define data
    """
    data = {}
    data['nation'] = 'Israel'
    data['description'] = 'Israel by age'
    data['source'] = 'Israel Ministry of Health'
    data['source_url'] = 'https://data.gov.il/dataset/covid-19'

    # common regional abbreviations used in the data files
    regional_abbreviations = {
        'Under 20': '19',
        '20s': '20',
        '30s': '30',
        '40s': '40',
        '50s': '50',
        '60s': '60',
        '70s': '70',
        'Over 79': '80',
        'Unknown': 'xx',
        'All': 'il'
    }

    files_data = {}
    filenames = ['il-pypm.csv','il-vacc-pypm.csv']
    sources = ['Israel Ministry of Health','Israel Ministry of Health']
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
    f1_populations = ['vaccinated']

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
