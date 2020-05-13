# -*- coding: utf-8 -*-
"""
Example of data description file: data.py

@author: karlen
"""

def get_data_description():
    """ Define data provided by BC CDC
    """
    data = {}
    data['nation'] = 'BC'
    data['description'] = 'BC cases by region, sex, age'
    data['source'] = 'BC CDC'
    data['source_url'] = 'http://www.bccdc.ca/health-info/diseases-conditions/covid-19/data'

    # categories
    categories = ['All','Male','Female','Fraser','Interior','Northern','Vancouver Coastal',
                  'Vancouver Island','<10','10-19','20-29','30-39','40-49','50-59','60-69','70-79',
                  '80-89','89+','Unknown']

    files_data = {}
    filenames = ['bc-pypm.csv']
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
    for category in categories:

        populations_data = {}
        f0_populations = ['reported']
        filename = filenames[0]
        for population in f0_populations:
            pop_data_total = {}
            pop_data_total['filename'] = filename
            header = ''
            if population == 'reported':
                header = category+'-pt'

            pop_data_total['header'] = header

            pop_data_daily = {}
            pop_data_daily['filename'] = filename
            header = ''
            if population == 'reported':
                header = category+'-pd'

            pop_data_daily['header'] = header

            population_data = {'daily': pop_data_daily, 'total': pop_data_total}
            populations_data[population] = population_data

        regions_data[category] = populations_data

    data['regional_data'] = regions_data

    return data

get_data_description()
