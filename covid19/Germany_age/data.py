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
    data['description'] = 'Germany by state and age'
    data['source'] = 'Robert Koch Institute'
    data['source_url'] = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html'

    # common regional abbreviations used in the data files
    regional_abbreviations = {
        'Germany':'de',
        'Baden-Wurttemberg':'bw',
        'Bavaria':'by',
        'North Rhine-Westphalia':'nw',
        'Saxony':'sn'
    }

    age_groups = {
        'A00-A04': 'a0',
        'A05-A14': 'a1',
        'A15-A34': 'a2',
        'A35-A59': 'a3',
        'A60-A79': 'a4',
        'A80+': 'a5'
    }

    files_data = {}
    filenames = ['germany-rki-age-pypm.csv']
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
        abbrev = regional_abbreviations[region]
        for age_group in age_groups:
            abbrev_age = '_'.join([abbrev,age_groups[age_group]])

            populations_data = {}

            f0_populations = ['reported', 'deaths']

            filename = filenames[0]
            for population in f0_populations:
                pop_data_total = {}
                pop_data_total['filename'] = filename
                header = ''
                if population == 'reported':
                    header = abbrev_age + '-pt'
                if population == 'deaths':
                    header = abbrev_age + '-dt'

                pop_data_total['header'] = header

                population_data = {'total': pop_data_total}
                populations_data[population] = population_data

            regions_data[abbrev_age] = populations_data

    data['regional_data'] = regions_data

    return data
