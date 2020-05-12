# -*- coding: utf-8 -*-
"""
Example of data description file: data.py

@author: karlen
"""

def get_data_description():
    """ Define data provided by Esri Canada
    """
    data = {}
    data['nation'] = 'Canada'
    data['description'] = 'Canada by province'
    data['source'] = 'Esri Canada'
    data['source_url'] = 'https://resources-covid19canada.hub.arcgis.com/'

    # common regional abbreviations used in the data files
    regional_abbreviations = {
        'BC':'BC',
        'Alberta':'AB',
        'Saskatchewan':'SK',
        'Manitoba':'MB',
        'Ontario':'ON',
        'Quebec':'QC',
        'New Brunswick':'NB',
        'Newfoundland':'NL',
        'Nova Scotia':'NS',
        'PEI':'PE',
        'Yukon':'YT',
        'NWT':'NT',
        'Nunavut':'NU'
        }


    files_data = {}
    filenames = ['ca-pypm.csv']
    for filename in filenames:
        file_data = {}
        file_data['source'] = 'More detailed information if folder has multiple sources'
        file_data['date header'] = 'Date'
        file_data['date start'] = [2020, 3, 1]

        files_data[filename] = file_data
    data['files'] = files_data

    #for each region, define location of each population data (file/column header)
    #either daily or total (or both) data can be provided

    regions_data = {}
    for region in regional_abbreviations:

        populations_data = {}
        f0_populations = ['reported', 'deaths',
                          'in_hospital', 'in_icu']
        filename = filenames[0]
        for population in f0_populations:
            pop_data_total = {}
            pop_data_total['filename'] = filename
            header = ''
            if population == 'reported':
                header = regional_abbreviations[region]+'-pt'
            if population == 'deaths':
                header = regional_abbreviations[region]+'-dt'
            if population == 'in_hospital':
                header = regional_abbreviations[region]+'-ht'
            if population == 'in_icu':
                header = regional_abbreviations[region]+'-it'

            pop_data_total['header'] = header

            population_data = {'total': pop_data_total}
            populations_data[population] = population_data

        regions_data[region] = populations_data

    data['regional_data'] = regions_data

    return data
