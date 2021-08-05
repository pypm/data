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
    data['source'] = 'JHU and Google Open Data'
    data['source_url'] = 'https://github.com/epiforecasts/covid19-forecast-hub-europe/tree/main/data-truth/JHU' \
                         ' and https://github.com/GoogleCloudPlatform/covid-19-open-data'

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
    filenames = ['eu-jhu-pypm.csv','eu-vacc-pypm.csv','eu-ecdc-pypm.csv']
    sources = ['JHU','Google','ECDC']
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
    f2_populations = ['hospitalized']

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

        filename = filenames[2]
        for population in f2_populations:
            pop_data_daily = {}
            pop_data_daily['filename'] = filename
            header = ''
            if population == 'hospitalized':
                header = regional_abbreviations[region] + '-hd'

            pop_data_daily['header'] = header

            population_data = {'daily': pop_data_daily}
            populations_data[population] = population_data

        regions_data[region] = populations_data

    data['regional_data'] = regions_data

    return data
