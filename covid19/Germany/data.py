# -*- coding: utf-8 -*-
"""
Example of data description file: data.py

@author: karlen
"""


def get_data_description():
    """ Define data provided by Robert Koch Institute
    """
    data = {}
    data['nation'] = 'Germany'
    data['description'] = 'Germany by state'
    data['source'] = 'Robert Koch Institute'
    data['source_url'] = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html'

    # common regional abbreviations used in the data files
    regional_abbreviations = {
        'Baden-Warttemberg':'bw',
        'Bavaria':'by',
        'Berlin':'be',
        'Brandenburg':'bb',
        'Bremen':'hb',
        'Hamburg':'hh',
        'Hesse':'he',
        'Lower Saxony':'ni',
        'Mecklenburg-Vorpommern':'mv',
        'North Rhine-Westphalia':'nw',
        'Rhineland-Palatinate':'rp',
        'Saarland':'sl',
        'Saxony':'sn',
        'Saxony-Anhalt':'st',
        'Schleswig-Holstein':'sh',
        'Thuringia':'th'
    }

    files_data = {}
    filenames = ['germany-pypm.csv']
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
                header = regional_abbreviations[region] + '-p'
            if population == 'deaths':
                header = regional_abbreviations[region] + '-d'

            pop_data_total['header'] = header

            population_data = {'total': pop_data_total}
            populations_data[population] = population_data

        regions_data[region] = populations_data

    data['regional_data'] = regions_data

    return data
