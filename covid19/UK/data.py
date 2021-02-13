# -*- coding: utf-8 -*-
"""
Example of data description file: data.py

@author: karlen
"""

def get_data_description():
    """ Define data
    """
    data = {}
    data['nation'] = 'England'
    data['description'] = 'England by region'
    data['source'] = 'Public Health England'
    data['source_url'] = 'https://www.gov.uk/government/publications/investigation-of-novel-sars-cov-2-variant-variant-of-concern-20201201'

    # common regional abbreviations used in the data files
    regional_abbreviations = {
        'East Midlands': 'EM',
        'East of England': 'EE',
        'London': 'LN',
        'North East': 'NE',
        'North West': 'NW',
        'South East': 'SE',
        'South West': 'SW',
        'West Midlands': 'WM',
        'Yorkshire and Humber': 'YH',
        'England': 'EN'
    }

    files_data = {}
    filenames = ['uk-pypm.csv']
    sources = ['Public Health England']
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
    f0_populations = ['reported', 'reported_v']

    for region in regional_abbreviations:

        populations_data = {}

        filename = filenames[0]
        for population in f0_populations:
            pop_data_total = {}
            pop_data_total['filename'] = filename
            header = ''
            if population == 'reported':
                header = regional_abbreviations[region]+'-pt'
            if population == 'reported_v':
                header = regional_abbreviations[region]+'-qt'

            pop_data_total['header'] = header

            population_data = {'total': pop_data_total}
            populations_data[population] = population_data

        regions_data[region] = populations_data

    data['regional_data'] = regions_data

    return data
