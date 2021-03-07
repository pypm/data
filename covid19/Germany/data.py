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
    data['source'] = 'Robert Koch Institute, DIVI, Google Open Data'
    data['source_url'] = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html '\
                         'https://www.divi.de/' \
                         ' and https://github.com/GoogleCloudPlatform/covid-19-open-data'

    # common regional abbreviations used in the data files
    regional_abbreviations = {
        'Germany':'de',
        'Baden-Wurttemberg':'bw',
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
    filenames = ['germany-rki-pypm.csv','germany-divi-pypm.csv','germany-vacc-pypm.csv']
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
        f1_populations = ['in_icu', 'on_ventilator']
        f2_populations = ['vaccinated']

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
            if population == 'in_icu':
                header = regional_abbreviations[region]+'-ic'
            if population == 'on_ventilator':
                header = regional_abbreviations[region]+'-vc'

            pop_data_total['header'] = header

            population_data = {'total': pop_data_total}
            populations_data[population] = population_data

        filename = filenames[2]
        for population in f2_populations:
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
