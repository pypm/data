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

    populations = {'reported':{'total':{'header':'-pt','fileid':0}},
                   'deaths': {'total': {'header': '-dt', 'fileid': 0}},
                   'icu admissions': {'total': {'header': '-it', 'fileid': 0},'daily': {'header': '-id', 'fileid': 0}},
                   'in_icu': {'total': {'header': '-ic', 'fileid': 0}},
                   'hospitalized': {'total': {'header': '-ht', 'fileid': 0}, 'daily': {'header': '-hd', 'fileid': 0}},
                   'in_hospital': {'total': {'header': '-hc', 'fileid': 0}},
                   'vaccinated': {'total': {'header': '-xt', 'fileid': 1}}
                   }

    regions_data = {}
    for region in regional_abbreviations:

        populations_data = {}
        for population in populations:
            population_data = {}
            for data_type in populations[population]:
                info = populations[population][data_type]
                header = regional_abbreviations[region] + info['header']
                population_data[data_type] = {'header':header, 'filename':filenames[info['fileid']]}
            populations_data[population] = population_data

        regions_data[region] = populations_data

    data['regional_data'] = regions_data

    return data
